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

    def put_image(self, path_on_cloud, path_local, token):
        self.storage.child(path_on_cloud).put(path_local, token)

    def put_txt(self, path_on_cloud, path_local):
        self.storage.child(path_on_cloud).put(path_local)

    def download_image(self, path_on_cloud, path_local):
        self.storage.child(path_on_cloud).download(path_local)

    def get_url(self, path_on_cloud):
        return self.storage.child(path_on_cloud).get_url(None)

    def get_all_urls(self):
        all_files = self.storage.list_files()
        return [{'path': file_.name, 'url': self.get_url(file_.name)} for file_ in all_files]

    def get_all_register_urls(self):
        all_files = self.storage.list_files()
        return [path.name for path in all_files if 'register/photos' in path.name]

    def get_all_augment_urls(self):
        all_files = self.storage.list_files()
        return [path.name for path in all_files if 'augment/photos' in path.name]

    def filter_crop_photos(self, urls_data):
        result = []
        for item in urls_data:
            photo_type = item['path'].split('/')[1]
            photo_name = item['path'].split('/')[2]
            if photo_type == 'augment' and photo_name == '0.jpg':
                result.append(item)
        return result
