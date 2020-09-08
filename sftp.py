#!/usr/bin/env python
# coding: utf-8


import datetime
import pysftp
import os,shutil
from pathlib import Path
import pathlib

#log function to log the message
def log(message,filename):
    f = open("logfile.log", "a")
    f.write(str(datetime.datetime.now())+" | "+message+" | "+filename+"\n")
    f.close()
#move the file to Failure folder
def moveFileToFailure(filename,local_path): 
    try:
        shutil.move(local_path+"/datauploads/"+filename,local_path+"/datauploads/Failure/"+filename)
        log("Moved to Failure folder",file_name)
    except Exception as e:
        print(e)
        log("Failed to move to Failure folder",file_name)
#move the file to Success folder
def moveFileToSuccess(filename,local_path):
    try:
        #move command tp move the file with source and destination path
        shutil.move(local_path+"/datauploads/"+filename,local_path+"/datauploads/Success/"+filename)
        log("Moved to Success folder",file_name)
    except Exception as e:
        print(e)
        log("Failed to move to Success folder",file_name)

def uploadfile():
    #remote log url , username, password and port num 
    host = 'localhost'
    port = 22
    username = 'uname'
    password='pass'
    cnopts = pysftp.CnOpts(knownhosts='known_hosts')
    cnopts.hostkeys = None
    #list of files from datauploads folder
    #dataupload 
    files = os.listdir(Path('datauploads'))
    #local path where .py file is located 
    local_path=str(pathlib.Path().absolute())
    #remote path where you want to upload the file 
    remote_path_touploadfile='Downloads'
    for file_name in files:
        #file path from dataupload folder
        local_file_path=local_path+"/datauploads/"+file_name
        #check is file to upload
        if os.path.isfile(local_file_path):
            try:
                #pysftp Connection function to connect with remote server
                with pysftp.Connection(host, username=username,port=port, password=password,cnopts=cnopts) as sftp:
                    #change current working directory
                    with sftp.cd(remote_path_touploadfile):
                        #remote servers cwd
                        remotepath=sftp.getcwd()
                        #pysft put function to upload from local to remote server
                        sftp.put(localpath=local_file_path)
                        #gets file size after upload
                        remotefilesize=sftp.stat(remotepath=remotepath+"/"+file_name).st_size
                        #gets file size of orignal file
                        localfilesize=Path(local_file_path).stat().st_size
                        if (remotefilesize !=localfilesize):
                            log("Failed to upload",file_name)
                            moveFileToFailure(file_name,local_path)
                        else:
                            log("Successfully uploaded",file_name)
                            moveFileToSuccess(file_name,local_path)
            except Exception as e:
                print(e)
                log("Failed to upload",file_name)
                moveFileToFailure(file_name,local_path)

uploadfile()

