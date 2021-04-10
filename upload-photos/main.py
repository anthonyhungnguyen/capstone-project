import drive_source
import firebase_target
import crop_and_augment
from tqdm import tqdm
import uuid
FACE_SERVER = "http://localhost:5000"

drive_instance = drive_source.Drive()
firebase_instance = firebase_target.FireBase()
face_instance = crop_and_augment.CropAndAugment(FACE_SERVER)

drive = drive_instance.authorize_drive()


def sync_all_register_photos():
    all_students_folder = drive_instance.load_all_folders_files(
        drive, drive_instance.ROOT_ID)
    for folder_ in tqdm(all_students_folder):
        student_id = folder_['title']
        student_files = drive_instance.load_all_folders_files(
            drive, folder_['id'])
        for index, file_ in enumerate(student_files):
            drive_instance.save_image_by_id(drive, file_['id'], 'temp.jpg')
            firebase_instance.put_image(
                f"{student_id}/register/{index}.jpg", './temp.jpg', str(uuid.uuid4()))


def save_augment_photos():
    all_files = firebase_instance.storage.list_files()
    track_list = []
    for file_ in tqdm(all_files):
        try:
            path_list = file_.name.split('/')
            student_id = path_list[0]
            if student_id in track_list:
                continue
            track_list.append(student_id)
            firebase_instance.download_image(file_.name, './raw.jpg')
            face_instance.crop('./raw.jpg')
            face_instance.augment('./crop.jpg')
            firebase_instance.put_image(
                f"{student_id}/augment/0.jpg", './crop.jpg', str(uuid.uuid4()))
            for i in range(4):
                firebase_instance.put_image(
                    f"{student_id}/augment/0_{i}.jpg", f'./augment_{i}.jpg', str(uuid.uuid4()))
        except Exception:
            print(file_)


def get_urls():
    all_urls = firebase_instance.get_all_urls()
    print(firebase_instance.filter_crop_photos(all_urls))


get_urls()
