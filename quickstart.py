from __future__ import print_function
import pickle
import os.path
from googleapiclient.http import MediaFileUpload
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import glob
import pandas as pd
import numpy as np
import sqlalchemy as sql
import shutil

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.appdata',
          'https://www.googleapis.com/auth/drive.scripts',
          'https://www.googleapis.com/auth/drive.apps.readonly',
          'https://www.googleapis.com/auth/drive.metadata']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    print('[Master] Iniciando atualização')

    if os.path.exists('Credentials/token.pickle'):
        print('[Master] Encontrado Token')
        with open('Credentials/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('[Master] Atualizando credenciais')
            creds.refresh(Request())
        else:
            print('[Master] Procurando credencial')
            flow = InstalledAppFlow.from_client_secrets_file(
                'Credentials/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        print('[Master] Criando Token')
        with open('Credentials/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    print('[Google Drive] Conectando Serviço')
    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    print('[Google Drive] Procurando Arquivos')
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('[Google Drive] Nenhum arquivo encontrado!')

    print('[MySQL | MariaDB] Procurando autorização')
    with open('Credentials/credentials.txt', 'r', encoding='utf-8') as f:
        credential = f.read()

    print('[MySQL | MariaDB] Conectando')
    db = sql.create_engine('mysql+pymysql://' + credential)

    print('[MySQL | MariaDB] Coletando arquivos SQL')
    for path in glob.glob('Query/*.sql'):
        with open(path, 'r', encoding='utf-8') as line:
            query = line.read()
            print('[MySQL | MariaDB] (Executando) '+query+'\n')
            df = pd.read_sql_query(query, db)
        file = path.split('\\')[1][:-4]+'.tsv'
        folder_name = 'temp'
        print('[Master] Criando arquivo temporário')
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        print('[Master] (Criando) '+folder_name+'/'+file)
        df.to_csv(folder_name+'/'+file, sep='\t', index=False)

        print('[Google Drive] Procurando arquivo')
        has = [item for item in items if item['name']==file]
        if any(has):
            print('[Google Drive] Atualizando: '+file)
            update_file(service=service,
                   file_id=has[0]['id'],
                   new_mime_type='application/vnd.google-apps.spreadsheet',
                   new_filename=has[0]['name'],
                   folder_name=folder_name)
        else:
            print('[Google Drive] Enviando: '+file)
            upload_file(service=service,
                        new_mime_type='application/vnd.google-apps.spreadsheet',
                        new_filename=file,
                        folder_name=folder_name)
    print('[Master] Excluindo diretório temporário')
    shutil.rmtree(folder_name)
    print('[Master] Concluído !')

def upload_file(service, new_mime_type, new_filename, folder_name):
  """Upload a new file's metadata and content.

  Args:
    service: Drive API service instance.
    new_mime_type: New MIME type for the file.
    new_filename: Filename of the new content to upload.
    folder_name: Folder where is the file
  Returns:
    Updated file metadata if successful, None otherwise.
  """
  try:
    # File's new content.
    file_metadata = {'name': new_filename,
                     'mimeType': new_mime_type}
    media_body = MediaFileUpload(folder_name+'/'+new_filename,
                                 mimetype='text/csv',
                                 resumable=True)

    # Send the request to the API.
    file = service.files().create(body=file_metadata,
                                  media_body=media_body,
                                  fields='id').execute()
    return file
  except errors.HttpError as error:
    print('[Google Drive] Ocorreu um erro: %s' % error)
    return None

def update_file(service, file_id, new_mime_type, new_filename, folder_name):
  """Update an existing file's metadata and content.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to update.
    new_mime_type: New MIME type for the file.
    new_filename: Filename of the new content to upload.
    folder_name: Folder where is the file
  Returns:
    Updated file metadata if successful, None otherwise.
  """
  try:
    # First retrieve the file from the API.
    file = service.files().get(fileId=file_id).execute()

    # File's new metadata.
    file['mimeType'] = new_mime_type

    # File's new content.
    body = {'appProperties': {'my_key': 'updated_my_value'}}
    media_body = MediaFileUpload(folder_name+'/'+new_filename,
                                 mimetype=new_mime_type,
                                 resumable=True)

    # Send the request to the API.
    updated_file = service.files().update(fileId=file_id,
                                          body=body,
                                          media_body=media_body).execute()
    return updated_file
  except errors.HttpError as error:
    print('[Google Drive] Ocorreu um erro: %s' % error)
    return None

if __name__ == '__main__':
    main()

