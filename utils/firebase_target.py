import pyrebase


class FireBase:
    def __init__(self):
        self.config = {"apiKey": "AIzaSyDvyKgZQdDzn49T_QX-vox-RwawATduCo0",
                       "authDomain": "capstone-bk.firebaseapp.com",
                       "projectId": "capstone-bk",
                       "storageBucket": "capstone-bk.appspot.com",
                       "messagingSenderId": "616596048413",
                       "databaseURL": "https://capstone-bk-default-rtdb.firebaseio.com",
                       "appId": "1:616596048413:web:97990995ad196f04d854f4",
                       "serviceAccount": "./serviceAccount.json"}
        self.firebase = pyrebase.initialize_app(self.config)
        self.storage = self.firebase.storage()

    def put_image(self, path_on_cloud, path_local):
        self.storage.child(path_on_cloud).put(path_local)

    def download_image(self, path_on_cloud, path_local):
        self.storage.child(path_on_cloud).download(path_local)
