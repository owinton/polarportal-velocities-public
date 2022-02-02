import ftplib
import os
import shutil

"""
Created by kaha on 25 Jun 2018
Last edited by oew on 10 Mar 2021
"""
def IV_ftp_upload(output_plots_to_upload, output_plots_uploaded):
	#ftp = ftplib.FTP('ftpserver.dmi.dk')
	ftp = ftplib.FTP('ftp.dlptest.com')
	with open('../username_password.txt', 'r') as file:
    	data = file.readlines()
    	data = [d.replace('\n', '') for d in data]
	USERNAME = data[2]
	PASSWORD = data[3]
	#ftp.login(USERNAME, PASSWORD)	
	ftp.login('dlpuser', 'rNrKYTX9g7z3RgJRmxWuGHbeu')
	#ftp.cwd('upload')
	upload_list = [i for i in output_plots_to_upload if i.endswith('.png')]
	for upload_filename in upload_list:
		file = open(os.path.join(output_plots_to_upload, upload_filename, 'rb')
		ftp.storbinary(upload_filename, file)
		print('Uploaded {}'.format(filename))
		shutil.move(os.path.join(output_plots_to_upload, upload_filename), os.path.join(output_plots_uploaded, upload_filename))
	ftp.quit()
