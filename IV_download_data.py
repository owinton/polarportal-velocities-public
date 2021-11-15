from pyDataverse.api import NativeApi, DataAccessApi
import os
'''
Function to download velocity data from from GEUS dataverse

Created by Øyvind Andreas Winton (oew) on 10 Mar 2021
Last edited by oew on 10 Mar 2021

'''
def IV_download_data():
	data_directory = './data/IV_data/' # the directory to which velocity files should be downloaded
	local_files_list = [i for i in os.listdir(data_directory) if i.endswith('.nc')]
	n_local = len(local_files_list)

	# Setup of pyDataverse structures to download velocity data sets
	base_url = "https://dataverse01.geus.dk"
	api = NativeApi(base_url)
	data_api = DataAccessApi(base_url)
	DOI = "doi:10.22008/promice/data/sentinel1icevelocity/greenlandicesheet"
	dataset = api.get_dataset(DOI)


	remote_files_list = dataset.json()['data']['latestVersion']['files']
	# Download only netcdf files
	remote_files_list = [i for i in remote_files_list if (i['dataFile']['contentType'] == 'application/x-netcdf')]
	n_available = len(remote_files_list)

	# Download only files that are not already downloaded
	remote_files_list = [i for i in remote_files_list if (i['dataFile']['filename'] not in local_files_list)]
	n_download = len(remote_files_list)
	print('Downloading {} files of {} available. {} files already stored locally'.format(n_download, n_available, n_local))
	for file in remote_files_list:
		filename = file["dataFile"]["filename"]
		file_id = file["dataFile"]["id"]
		if (filename.endswith('.nc')) & (filename not in local_files_list):
			response = data_api.get_datafile(file_id)
			with open('{}/{}'.format(data_directory, filename), "wb") as f:
				f.write(response.content)
				print('Downloaded {}'.format(filename))
