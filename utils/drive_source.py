from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Drive:
    def __init__(self):
        self.ROOT_ID = "1NaHxdOIK-KDfR0nWDOyDmezpyZOKUdmI"

    def generate_credentials(self, credentials_filename):
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(credentials_name)
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")

    def authorize_drive(self):
        gauth = GoogleAuth()
        gauth.DEFAULT_SETTINGS['client_config_file'] = "client_secrets.json"
        gauth.LoadCredentialsFile("mycreds.txt")
        return GoogleDrive(gauth)

    def load_all_folders_files(self, drive, root_id):
        query = f"'{root_id}' in parents and trashed = false"
        file_list = drive.ListFile({'q': query}).GetList()
        return [{"title": file['title'], "id": file['id']} for file in file_list]

    def save_image_by_id(self, drive, id, file_name):
        file1 = drive.CreateFile({"id": id})
        file1.GetContentFile(file_name)
    
    def upload_folder(self, folder_name):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = drive_service.files().create(body=file_metadata,
                                            fields='id').execute()

