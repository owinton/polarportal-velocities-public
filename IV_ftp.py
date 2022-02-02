import ftplib
import os
import shutil

"""
Function for uploading images to the DMI server.

Inputs:
    output_plots_to_upload: string with path to folder containing the images to be uploaded to the server
    output_plots_uploaded: string with path to folder in which to place uploaded images
    

Created by kaha on 25 Jun 2018
Last edited by oew on 02 Feb 2022
"""
def IV_ftp_upload(output_plots_to_upload, output_plots_uploaded):
    ftp = ftplib.FTP('ftpserver.dmi.dk')
    print(ftp.getwelcome());

    # Credentials are stored in txt file not shared in the public repo.
    with open('../username_password.txt', 'r') as file:
        data = file.readlines()
        data = [d.replace('\n', '') for d in data]
    USERNAME = data[2]
    PASSWORD = data[3]

    ftpResponse = ftp.login(USERNAME, PASSWORD)
    print(ftpResponse)
    ftpResponse = ftp.cwd('upload')
    print(ftpResponse)

    upload_list = [i for i in os.listdir(output_plots_to_upload) if i.endswith('.png')]
    for upload_filename in upload_list:
        file = open(os.path.join(output_plots_to_upload, upload_filename), 'rb')
        ftpCommand = "STOR {}".format(upload_filename);
        ftpResponse = ftp.storbinary(ftpCommand, file)
        print(ftpResponse)
        print('Uploaded {}'.format(upload_filename))
        shutil.move(os.path.join(output_plots_to_upload, upload_filename), os.path.join(output_plots_uploaded, upload_filename))
    ftp.quit()