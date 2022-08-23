import os
from IV_flowline_timeseries import IV_flowline_timeseries
from IV_mean import IV_mean
from IV_download_data import IV_download_data
from IV_ftp import IV_ftp_upload
'''
Script for creating flow line time series of velocities for various glaciers.

Requires directories as below
    IV_dir: directory with velocity-data. Containing filenames of type 'IV_YYYYMMDD_YYYYMMDD.nc'
    IV_mean_dir: directory with average velocity-data. Containing filenames of type 'IV_mean_YYYYMMDD_to_YYYYMMDD.npy'
    CFL_dir: directory with calving front lines. Containing structures of type '79F_frontlines_4326/79F2018/79F2018.shp'
    outdir: directory where output plots are saved, and existence of previous plots are checked
    FL_dir: directory containing flowlines of glaciers. Containing filenames of type '79F.txt'
    cm_file: file containing colormap specification for IV on logarithmic scale. Lines of e.g. 0.01,58,84,161,255,0.010
    glaciers: List containing strings with glacier names in the specified format
    
Calls the following functions
    IV_mean: function for returning l average velocity. Calculates the latest average if a new SMB-year has ended (September)
    IV_flowline_timeseries: Function for creating a flowline figure of velocities for a given glacier.
    

Created by Øyvind Andreas Winton (oew) on 12 February 2020
'''

IV_dir = './data/IV_data'
IV_mean_dir = './data/IV_mean'
CFL_dir = './data/Glacier_front_lines/line'
FL_dir = './data/Flowlines'
bed_file =  './data/BedMachineGreenland-2017-09-20.nc'
output_plots_to_upload = './output_plots_to_upload'
output_plots_uploaded = './output_plots_uploaded'
sep = '/'
cm_file = './data/iv_colormap.txt'

# All glaciers on Polarportal (Upernavik and Ikertivaq divided in smaller)
glaciers = [
'Ryder', 
'Petermann', 
'Humboldt', 
'Steenstrup', 
'Hayes', 
'Nunatakassaap_Sermia', 
'UpernavikA',
'UpernavikB',
'UpernavikC',
'UpernavikD',
'UpernavikE',
'UpernavikF',
'Kangigdleq',
'Store',
'Jakobshavn',
'KNS',
'Ostenfeld',
'79F',
'Zachariae',
'Storstrommen',
'DaugaardJensen',
'Kangerdlugssuaq',
'Midgaard',
'Helheim',
'IkertivaqA',
'IkertivaqB',
'IkertivaqC',
'IkertivaqD',]
glaciers = ['Jakobshavn']

# Download new velocity files, get list of files, and get/create most recent mean velocity file
# IV_download_data()
IV_list = [i for i in (os.listdir(IV_dir)) if i.endswith('.nc')]
IV_list.sort()
mean_IV_file = IV_mean(IV_dir, IV_mean_dir)

# For each file, process all glaciers
for file in IV_list:
    IV_file = IV_dir + '/' + file
    year = IV_file[-20:-16]
    CFL_year = '2018' # Use same year for calving front line for now #TODO Make dynamic in CFL.
    for glacier in glaciers:
        filename = '/' + glacier + '_' + IV_file[-20:-3] + '_IV_timeseries.png'
        if (filename not in os.listdir(output_plots_uploaded)) & (filename not in os.listdir(output_plots_to_upload)): # check if file exists, if not create it
            outfile = output_plots_to_upload + sep + filename
            CFL_file = CFL_dir + sep + glacier + '_frontlines_4326' + sep + glacier + CFL_year + sep + glacier + CFL_year + '.shp'
            FL_file = FL_dir + sep + glacier + '.txt'
            #IV_flowline_timeseries(glacier, IV_file, CFL_file, FL_file, cm_file, outfile, mean_IV_file, bed_file)

IV_ftp_upload(output_plots_to_upload, output_plots_uploaded)
