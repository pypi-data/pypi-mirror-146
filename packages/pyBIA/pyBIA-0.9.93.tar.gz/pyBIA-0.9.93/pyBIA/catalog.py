from warnings import warn

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.stats import sigma_clipped_stats

from photutils.detection import DAOStarFinder
from photutils.aperture import aperture_photometry, CircularAperture, CircularAnnulus
from photutils import detect_threshold
from astropy.convolution import Gaussian2DKernel
from astropy.stats import gaussian_fwhm_to_sigma
from photutils import detect_sources
from photutils.segmentation import SourceCatalog

from pyBIA import data_processing

def create(data, error=None, morph_params=True, x=None, y=None, obj_name=None, field_name=None, flag=None, 
    aperture=15, annulus_in=20, annulus_out=35, invert=False, nsig=2, save_file=True, path='', filename=None):
    """
    Creates a photometric and morphological catalog containing the object(s) in 
    the given position(s) at the given order. The parameters x and y should be 1D 
    arrays containing the pixel location of each source. The input can be for a 
    single object or multiple objects.

    If no positions are input then a catalog is automatically 
    generated using the DAOFIND algorithm. Sources with local density
    maxima greater than nsig standard deviations from the background. 
    
    Example:
        We can use the world coordinate system in astropy
        to convert ra/dec to pixels and then call pyBIA.catalog:

        >>> import astropy
        >>> from pyBIA import catalog

        >>> hdu = astropy.io.fits.open(name)
        >>> wcsobj= astropy.wcs.WCS(header = hdu[0].header)

        >>> x_pix, y_pix = wcsobj.all_world2pix(ra, dec, 0) 
        >>> catalog.create(data, x_pix, y_pix)

    Args:
        data (ndarray): 2D array.
        error (ndarray, optional): 2D array containing the rms error map.
        morph_params (bool, optional): If True, image segmentation is performed and
            morphological parameters are computed. Defaults to True. 
        x (ndarray, optional): 1D array or list containing the x-pixel position.
            Can contain one position or multiple samples.
        y (ndarray, optional): 1D array or list containing the y-pixel position.
            Can contain one position or multiple samples.
        obj_name (ndarray, str, optional): 1D array containing the name of each object
            corresponding to the x & y position. This will be appended to the first
            column of the output catalog. Defaults to None.
        field_name (ndarray, str, optional): 1D array containing the field name of each object
            corresponding to the x & y positions. This will be appended to the first
            column of the output catalog. Defaults to None.
        flag (ndarray, optional): 1D array containing a flag value for each object corresponding
            to the x & y positions. Defaults to None. 
        aperture (int): The radius of the photometric aperture. Defaults to 15.
        annulus_in (int): The inner radius of the circular aperture
            that will be used to calculate the background. Defaults to 20.
        annulus_out (int): The outer radius of the circular aperture
                that will be used to calculate the background. Defaults to 35.
        invert (bool, optional): If True, the x & y coordinates will be switched
            when cropping out the object during the image segmentation step. For
            more information see the morph_parameters function. Defaults to False.
        nsig (int): Objects in the image are detected if their peak intensity is
            higher than at least nsig times the standard deviation derived from
            sigma-clipped statistics. Default is 2.
        save_file (bool): If set to False then the catalog will not be saved to the machine. 
            You can always save manually, for example, if df = catalog(), then you can save 
            with: df.to_csv('filename'). Defaults to True.
        path (str, optional): By default the text file containing the photometry will be
            saved to the local directory, unless an absolute path to a directory is entered here.
        filename(str, optional): Name of the output catalog. Default name is 'pyBIA_catalog'.

    Note:
        As Lyman-alpha nebulae are diffuse sources with
        extended emission features, the default radius of
        the circular photometric aperture is 15 pixels. This 
        large aperture allows us to encapsulate the largest blobs.
    
        The background is calculated as the median pixel value
        within the area of the annulus. Increasing the size of the
        annulus may yield more robust background measurements. This
        is especially important when extracting photometry in crowded fields
        where surrounding sources may skew the median background.
                
    Returns:
        A catalog of all objects input (or automatically detected if there were no position arguments), 
        containing both photometric and morphological information. A CSV file titled "pyBIA_catalog" 
        will also be saved to the local directory, unless an absolute path argument is specified.
          
    """
    
    if error is not None:
        if data.shape != error.shape:
            raise ValueError("The rms error map must be the same shape as the data array.")
    if aperture > annulus_in or annulus_in > annulus_out:
        raise ValueError('The radius of the inner and out annuli must be larger than the aperture radius.')
    if x is not None:
        try: #If position array is a single number it will be converted to a list of unit length
            len(x)
        except TypeError:
            x, y = [x], [y]
        if len(x) != len(y):
            raise ValueError("The two position arrays (x & y) must be the same size.")
    if invert == False:
        warn('WARNING: Is your data from a .fits file? If so you may need to set invert=True if (x,y) = (0,0) is at the top left corner of the image instead of the bottom left corner.')
    if x is None: #Apply DAOFIND (Stetson 1987) to detect sources in the image
        mean, median, std = sigma_clipped_stats(data, sigma=3.0)
        print('Performing source detection -- this will take several minutes...')
        daofind = DAOStarFinder(fwhm=3.0, threshold=2.*std)  
        sources = daofind(data - median)  
        for col in sources.colnames:  
            sources[col].info.format = '%.8g'      
        x, y = np.array(sources['xcentroid']), np.array(sources['ycentroid'])

    positions = []
    for j in range(len(x)):
        positions.append((x[j], y[j]))

    apertures = CircularAperture(positions, r=aperture)
    annulus_apertures = CircularAnnulus(positions, r_in=annulus_in, r_out=annulus_out)
    annulus_masks = annulus_apertures.to_mask(method='center')
    annulus_data = annulus_masks[0].multiply(data)
    mask = annulus_masks[0].data
    annulus_data_1d = annulus_data[mask > 0]
    median_bkg = np.median(annulus_data_1d)
        
    if error is None:
        phot_table = aperture_photometry(data, apertures)
        flux = phot_table['aperture_sum'] - (median_bkg * apertures.area)
        if morph_params == True:
            prop_list = morph_parameters(data, x, y, invert=invert)
            tbl = make_table(prop_list)
            df = make_dataframe(table=tbl, x=x, y=y, obj_name=obj_name, field_name=field_name, flag=flag,
                flux=flux, save=save_file, path=path)
            return df

        df = make_dataframe(table=None, x=x, y=y, obj_name=obj_name, field_name=field_name, flag=flag, 
            flux=flux, save=save_file, path=path)
        return df
       
    phot_table = aperture_photometry(data, apertures, error=error)
    flux = phot_table['aperture_sum'] - (median_bkg * apertures.area)
    flux_err = phot_table['aperture_sum_err']
    if morph_params == True:
        prop_list = morph_parameters(data, x, y, invert=invert)
        tbl = make_table(prop_list)
        df = make_dataframe(table=tbl, x=x, y=y, obj_name=obj_name, field_name=field_name, flag=flag, 
            flux=flux, flux_err=flux_err, save=save_file, path=path)
        return df

    df = make_dataframe(table=None, x=x, y=y, obj_name=obj_name, field_name=field_name, flag=flag, flux=flux, 
        flux_err=flux_err, save=save_file, path=path)
    return df


def morph_parameters(data, x, y, invert=False, nsig=2):
    """
    Applies image segmentation on each object to calculate morphological 
    parameters. These parameters can be used to train a machine learning classifier.
    
    Args:
        data (ndarray): 2D array.
        x (ndarray): 1D array or list containing the x-pixel position.
            Can contain one position or multiple samples.
        y (ndarray): 1D array or list containing the y-pixel position.
            Can contain one position or multiple samples.
        invert (bool): If True the x & y coordinates will be switched
            when cropping out the object, see Note below. Defaults to False.
        nsig (int): Objects in the image are detected if their peak intensity is
            higher than at least nsig times the standard deviation derived from
            sigma-clipped statistics. Default is 2.

    Note:
        This function requires x & y positions as each source 
        is isolated before the image segmentation is performed as this is
        computationally more efficient. If you need the x and y positions, you can
        run the catalog.create function, which will include the x & y pixel 
        positions of all cataloged sources.

        IMPORTANT: When loading data from a .fits file the pixel convention
        is switched. The (x, y) = (0, 0) position is on the top left corner of the .fits
        image. The standard convention is for the (x, y) = (0, 0) to be at the bottom left
        corner of the data. We strongly recommend you double-check your data coordinate
        convention. We made use of .fits data with the (x, y) = (0, 0) position at the top
        left of the image, for this reason we switched x and y when cropping out individual
        objects. The parameter invert=True performs the coordinate switch for us. This is only
        required because pyBIA's cropping function assumes standard convention.
    
    Return:
        A catalog of morphological parameters. If multiple positions are input, then the
        output will be a list containing multiple morphological catalogs, one for
        each position.
        
    """

    if data.shape[0]<100 or data.shape[1]<100:
        raise ValueError('Data shape must be at least 100x100 to fit the required sub-array.')
    try: #If position array is a single number it will be converted into a list of unit length
        len(x)
    except TypeError:
        x, y = [x], [y]

    prop_list=[]
    print('Applying image segmentation, this could take a while...')
    for i in range(len(x)):
        new_data = data_processing.crop_image(data, int(x[i]), int(y[i]), 100, invert=invert)
        threshold = detect_threshold(new_data, nsigma=nsig)

        sigma = 3.0 * gaussian_fwhm_to_sigma   
        kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
        kernel.normalize()
        segm = detect_sources(new_data, threshold, npixels=5, kernel=kernel)
        try:
            props = SourceCatalog(new_data, segm, kernel=kernel)
        except:
            warn('At least one object could not be detected in segmentation... perhaps the object is too faint or there is a coordinate error. NOTE: This object is still in the catalog, the morphologcail features have been set to zero.')
            prop_list.append(0)
            continue

        sep_list=[]
        for xx in range(len(props)): #This is to select the segmented object closest to the center, (x,y)=(50,50)
            xcen = float(props[xx].centroid[0])
            ycen = float(props[xx].centroid[1])
        
            sep = np.sqrt((xcen-50)**2 + (ycen-50)**2)
            sep_list.append(sep)

        inx = np.where(sep_list == np.min(sep_list))[0]
        if len(inx) > 1:
            inx = inx[0]

        prop_list.append(props[inx])

    return np.array(prop_list)

def make_table(props):
    """
    Returns the morphological parameters calculated from the sementation image.
    A list of the parameters and their function is available in the Photutils
    Source Catalog documentation: https://photutils.readthedocs.io/en/stable/api/photutils.segmentation.SourceCatalog.html
    
    Args:
        Props (source catalog): A source catalog containing the 30 segmentation parameters.
        
    Returns:
        Array containing the morphological features. 

    """

    table = []
    for i in range(len(props)):
        prop_list = []
        try:
            props[i][0].area
        except:
            for j in range(30): #number of morphological params
                prop_list.append(0)
            table.append(prop_list)
            continue

        prop_list.append(float(props[i][0].area / u.pix**2))
        prop_list.append(props[i][0].bbox_xmax)
        prop_list.append(props[i][0].bbox_xmin)
        prop_list.append(props[i][0].bbox_ymax)
        prop_list.append(props[i][0].bbox_ymin)
        prop_list.append(props[i][0].bbox.shape[0] * props[i][0].bbox.shape[1])
        prop_list.append(float(props[i][0].covar_sigx2 / u.pix**2))
        prop_list.append(float(props[i][0].covar_sigxy / u.pix**2))
        prop_list.append(float(props[i][0].covar_sigy2 / u.pix**2))
        prop_list.append(float(props[i][0].covariance_eigvals[0] / u.pix**2))
        prop_list.append(float(props[i][0].covariance_eigvals[1] / u.pix**2))
        prop_list.append(float(props[i][0].cxx * u.pix**2))
        prop_list.append(float(props[i][0].cxy * u.pix**2))
        prop_list.append(float(props[i][0].cyy * u.pix**2))
        prop_list.append(float(props[i][0].eccentricity))
        prop_list.append(float(props[i][0].ellipticity))
        prop_list.append(float(props[i][0].elongation))
        prop_list.append(float(props[i][0].equivalent_radius / u.pix))
        prop_list.append(float(props[i][0].fwhm / u.pix))
        prop_list.append(props[i][0].gini)
        prop_list.append(props[i][0].kron_flux)
        prop_list.append(float(props[i][0].kron_radius / u.pix))
        prop_list.append(props[i][0].max_value)
        prop_list.append(props[i][0].min_value)
        prop_list.append(float(props[i][0].orientation / u.degree))
        prop_list.append(float(props[i][0].perimeter / u.pix))
        prop_list.append(props[i][0].segment_flux)
        prop_list.append(float(props[i][0].semimajor_sigma / u.pix))
        prop_list.append(float(props[i][0].semiminor_sigma / u.pix))

        if props[i][0].isscalar == True: #Checks whether it's a single source
            prop_list.append(1)
        else:
            prop_list.append(0)
        table.append(prop_list)

    return np.array(table)

def make_dataframe(table=None, x=None, y=None, flux=None, flux_err=None, obj_name=None,
    field_name=None, flag=None, save=True, path=None, filename=None):
    """
    This function takes as input the catalog of morphological features
    which is output by the make_cat_tbl function -- this catalog is converted
    into a Pandas dataframe. 


    Args:
        table (optional): Table containing the object features. Can make with make_table() function.
            If None then a Pandas dataframe containing only the input columns will be generated. Defaults to None.
        x (ndarray, optional): 1D array containing the x-pixel position.
            If input it must be an array of x positions for all objects in the table. 
            This x position will be appended to the dataframe for cataloging purposes. Defaults to None.
        y (ndarray, optional): 1D array containing the y-pixel position.
            If input it must be an array of y positions for all objects in the table. 
            This y position will be appended to the dataframe for cataloging purposes. Defaults to None.
        flux (ndarray, optional): 1D array containing the calculated flux
            of each object. This will be appended to the dataframe for cataloging purposes. Defaults to None.
        flux_err (ndarray, optional): 1D array containing the calculated flux error
            of each object. This will be appended to the dataframe for cataloging purposes. Defaults to None.
        name (ndarray, str, optional): A corresponding array or list of object name(s). This will be appended to 
            the dataframe for cataloging purposes. Defaults to None.
        flag (ndarray, optional): 1D array containing a flag value for each object corresponding
            to the x & y positions. Defaults to None. 
        save (bool, optional): If False the dataframe CSV file will not be saved to the local
            directory. Defaults to True. 
        path (str, optional): Absolute path where CSV file should be saved, if save=True. If 
            path is not set, the file will be saved to the local directory.
        filename(str, optional): Name of the output catalog. Default name is 'pyBIA_catalog'.


    Note:
        These features can be used to create a machine learning model. 

    Example:

        >>> props = morph_parameters(data, x=xpix, y=ypix)
        >>> table = make_table(props)
        >>> dataframe = make_dataframe(table, x=xpix, y=ypix)

    Returns:
        Pandas dataframe containing the parameters and features of all objects
        in the input data table. If save=True, a CSV file titled 'pybia_catalog'
        will be saved to the local directory, unless a path is specified.

    """
    if filename is None:
        filename = 'pyBIA_catalog'

    prop_list = ['area', 'bbox_xmax', 'bbox_xmin', 'bbox_ymax', 'bbox_ymin', 'bbox',
        'covar_sigx2', 'covar_sigxy', 'covar_sigy2', 'covariance_eigvals1', 'covariance_eigvals2',
        'cxx', 'cxy', 'cyy', 'eccentricity', 'ellipticity', 'elongation', 'equivalent_radius', 'fwhm',
        'gini', 'kron_flux', 'kron_radius', 'max_value', 'min_value', 'orientation', 'perimeter', 
        'segment_flux', 'semimajor_sigma', 'semiminor_sigma', 'isscalar' ]

    data_dict = {}

    if obj_name is not None:
        data_dict['obj_name'] = obj_name
    if field_name is not None:
        data_dict['field_name'] = field_name
    if flag is not None:
        data_dict['flag'] = flag
    if x is not None:
        data_dict['xpix'] = x
    if y is not None:
        data_dict['ypix'] = y
    if flux is not None:
        data_dict['flux'] = flux
    if flux_err is not None:
        data_dict['flux_err'] = flux_err
    
    if table is None:
        df = pd.DataFrame(data_dict)
        if save == True:
            if path is not None:
                df.to_csv(path+filename) 
                return df
            df.to_csv(filename)  
        return df

    try:
        len(table)
    except TypeError:
        table = [table]

    for i in range(len(table[0])):
        data_dict[prop_list[i]] = table[:,i]

    df = pd.DataFrame(data_dict)
    if save == True:
        if path is not None:
            df.to_csv(path+filename) 
            return df
        df.to_csv(filename)  
        return df
    return df

