#!/usr/bin/python3
from __future__ import print_function
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import auth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.metadata.readonly']

authInstance = auth.auth(SCOPES)
authCredentials=authInstance.getCredentials()

drive_service= build('drive', 'v3', credentials=authCredentials)


def listFiles(size):
    """ Lists  a number of files from your google drive directory"""
    results = drive_service.files().list(
        pageSize=size,
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))



#listFiles(100)


def CreateFolder(name):
    """ Creates a folder of given name on your google drive"""
    file_metadata= {
        'name':name,
        'mimeType':"application/vnd.google-apps.folder"
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ("Folder ID: {0}".format(file.get('id')))


#CreateFolder("testFolder")

def UploadFile(name,path,mimetype):
    """ Uploads a File of given name and mimetype"""
    file_metadata = {'name': name}
    media = MediaFileUpload(path,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ('File ID: %s' % file.get('id'))

#UploadFile("index.png","index.png","image/png")

