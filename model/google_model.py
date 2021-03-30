import pickle
import os.path
from googleapiclient.http import MediaFileUpload
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleDrive():
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.metadata']
        self.creds = None
        self.service = None
        self.items = None
        self.has = None
        self.file = None
        self.folder_id = None

    def create_folder(self, name):
        self.check_items(name)
        if not any(self.has):
            file_metadata = {
                 'name': name,
                 'mimeType': 'application/vnd.google-apps.folder'
            }
            file = self.service.files().create(body=file_metadata,
                                                 fields='id').execute()
            self.folder_id = file.get('id')
        else:
            self.folder_id = self.has[0]['id']

    def get_token(self, token_path='Credentials/token.pickle', secret_path='Credentials/client_secret.json'):
        if os.path.exists(token_path):
            print('[Master] Encontrado Token')
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print('[Master] Atualizando credenciais')
                self.creds.refresh(Request())
            else:
                print('[Master] Procurando credencial')
                flow = InstalledAppFlow.from_client_secrets_file(
                    secret_path, self.scopes)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            print('[Master] Criando Token')
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)

    def build_service(self):
        print('[Google Drive] Conectando Serviço')
        self.service = build('drive', 'v3', credentials=self.creds)

    def list_items(self):
        print('[Google Drive] Procurando Arquivos')
        results = self.service.files().list(
        fields="nextPageToken, files(id, name)").execute()
        self.items = results.get('files', [])

        if not self.items:
            print('[Google Drive] Nenhum arquivo encontrado!')

    def check_items(self, file):
        self.file = file
        print('[Google Drive] Procurando arquivo')
        self.has = [item for item in self.items if item['name'] == file]
        print('[Google Drive]'+(' Arquivo encontrado' if any(self.has) else ' Nenhum arquivo encontrado'))

    def upload_file(self, new_mime_type='application/vnd.google-apps.spreadsheet', folder_name='temp'):
        '''Upload a new file's metadata and content.

        Args:
            service: Drive API service instance.
            new_mime_type: New MIME type for the file.
            new_filename: Filename of the new content to upload.
            folder_name: Folder where is the file
        Returns:
            Updated file metadata if successful, None otherwise.
        '''
        try:
            file_metadata = {'name': self.file,
                             'parents': [self.folder_id],
                             'mimeType': new_mime_type}

            media_body = MediaFileUpload(folder_name+'/'+self.file,
                                         mimetype='text/csv',
                                         resumable=True)

            self.service.files().create(body=file_metadata,
                                          media_body=media_body,
                                          fields='id').execute()

        except errors.HttpError as error:
            print('[Google Drive] Ocorreu um erro: %s' % error)

    def update_file(self, new_mime_type='application/vnd.google-apps.spreadsheet', folder_name='temp'):
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
            file_id = self.has[0]['id']
            new_filename = self.has[0]['name']

            file = self.service.files().get(fileId=file_id).execute()

            # File's new metadata.
            file['mimeType'] = new_mime_type

            # File's new content.
            body = {'appProperties': {'my_key': 'updated_my_value'}}
            media_body = MediaFileUpload(folder_name + '/' + new_filename,
                                         mimetype=new_mime_type,
                                         resumable=True)

            # Send the request to the API.
            updated_file = self.service.files().update(fileId=file_id,
                                                  body=body,
                                                  media_body=media_body).execute()
            return updated_file
        except errors.HttpError as error:
            print('[Google Drive] Ocorreu um erro: %s' % error)
            return None