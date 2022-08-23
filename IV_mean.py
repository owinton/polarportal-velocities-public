import numpy as np
from netCDF4 import Dataset
import os
'''
Function for returning the latest average velocity. 
Creates a new average for the previous SMB-year if another full year of velocity data are available.


Inputs:
    IV_dir: string with directory to velocity data sets
    IV_mean_dir: string with directory to mean velocity data sets
Returns:
    String with directory+filename to latest mean velocity data set
    
Created by: Øyvind Andreas Winton (oew) on 25 February 2020
'''

def IV_mean(IV_dir, IV_mean_dir):
    # Sort lists of velocity and mean velocity maps
    IV_list = os.listdir(IV_dir)
    IV_list = [i for i in IV_list if i.endswith('.nc')]  # Only .nc files
    IV_list.sort()
    IV_mean_list = os.listdir(IV_mean_dir)
    IV_mean_list = [i for i in IV_mean_list if i.endswith('.npy')] # Only .npy files
    IV_mean_list.sort()

    # Get latest year and month of velocity data, what SMB year data are available for and the year of the latest mean
    latest_year = int(IV_list[-1][-11:-7])
    latest_month = int(IV_list[-1][-7:-5])
    if latest_month < 9: # The SMB year runs september-august
        smb_year = latest_year - 1
    else:
        smb_year = latest_year

    latest_mean = int(IV_mean_list[-1][-12:-8])
    if latest_mean < smb_year:  # Make new average if a full year SMB year of new velocities are acailable
        years_array = []
        print('Updating mean velocity with SMB-year %d' % (smb_year))
        for i, file in enumerate(IV_list):  # Get each velocity file
            print('{}. File {} of {}'.format(file, i+1, len(IV_list)))
            IV_data = Dataset(IV_dir + '/' + file, 'r')
            v_variable = IV_data.variables['land_ice_surface_velocity_magnitude'][:]
            v_std_variable = IV_data.variables['land_ice_surface_velocity_magnitude_std'][:]
            mask = v_variable.mask[0, :, :]
            v = v_variable.data[0, :, :]
            v_std = v_std_variable.data[0, :, :]
            uncertainty_mask = v_std > 0.5*v # Filter velocities with high relative uncertainty
            v[mask] = np.nan
            v[uncertainty_mask] = np.nan
            years_array.append(v)

            if i == 0:
                start_file = file
            # The last velocity dataset included is from the september of the current available smb-year
            elif (int(file[-11:-7]) == smb_year) and (int(file[-7:-5]) >= 9):  # Will advance only one year. Run script multiple times if e.g. latest mean is 2017 and there is data to make 2019
                stop_file = file
                break
        years_array = np.array(years_array)
        # mean = np.nanmean(years_array, axis=0)
        # std = np.nanstd(years_array, axis=0)
        quantiles = nan_percentile(years_array, [25, 50, 75])
        # lower_quantile = np.nanquantile(years_array, 0.25, axis=0)
        # median = np.nanquantile(years_array, 0.5, axis=0)
        # upper_quantile = np.nanquantile(years_array, 0.75, axis=0)
        filename = 'IV_mean_' + start_file[3:-12] + '_to_' + stop_file[12:-3]
        mean_IV_file = IV_mean_dir + '/' + filename
        # np.save(mean_IV_file, np.stack((mean, std)))
        np.save(mean_IV_file, np.stack((quantiles[0], quantiles[1], quantiles[2])))
        print('Mean velocity updated to SMB-year %d. Intentionally does not necesarily use all available files, only in whole SMB-years (sep-aug)' % (smb_year))
        return mean_IV_file + '.npy'
    else:
        mean_IV_file = IV_mean_dir + '/' + IV_mean_list[-1]
        return mean_IV_file


def nan_percentile(arr, q):
    '''
    Alternative to numpy's slow nanquantile, adapted from https://krstn.eu/np.nanpercentile()-there-has-to-be-a-faster-way/
    '''
    # valid (non NaN) observations along the first axis
    valid_obs = np.sum(np.isfinite(arr), axis=0)
    # replace NaN with maximum
    max_val = np.nanmax(arr)
    arr[np.isnan(arr)] = max_val
    # sort - former NaNs will move to the end
    arr = np.sort(arr, axis=0)

    # loop over requested quantiles
    if type(q) is list:
        qs = []
        qs.extend(q)
    else:
        qs = [q]
    if len(qs) < 2:
        quant_arr = np.zeros(shape=(arr.shape[1], arr.shape[2]))
    else:
        quant_arr = np.zeros(shape=(len(qs), arr.shape[1], arr.shape[2]))

    result = []
    for i in range(len(qs)):
        quant = qs[i]
        # desired position as well as floor and ceiling of it
        k_arr = (valid_obs - 1) * (quant / 100.0)
        f_arr = np.floor(k_arr).astype(np.int32)
        c_arr = np.ceil(k_arr).astype(np.int32)
        fc_equal_k_mask = f_arr == c_arr

        # linear interpolation (like numpy percentile) takes the fractional part of desired position
        floor_val = _zvalue_from_index(arr=arr, ind=f_arr) * (c_arr - k_arr)
        ceil_val = _zvalue_from_index(arr=arr, ind=c_arr) * (k_arr - f_arr)

        quant_arr = floor_val + ceil_val
        quant_arr[fc_equal_k_mask] = _zvalue_from_index(arr=arr, ind=k_arr.astype(np.int32))[fc_equal_k_mask]  # if floor == ceiling take floor value

        result.append(quant_arr)

    return result

def _zvalue_from_index(arr, ind):
    """private helper function to work around the limitation of np.choose() by employing np.take()
    arr has to be a 3D array
    ind has to be a 2D array containing values for z-indicies to take from arr
    See: http://stackoverflow.com/a/32091712/4169585
    This is faster and more memory efficient than using the ogrid based solution with fancy indexing.
    """
    # get number of columns and rows
    _,nC,nR = arr.shape

    # get linear indices and extract elements with np.take()
    idx = nC * nR * ind + np.arange(nC * nR).reshape((nC, nR))
    return np.take(arr, idx)
