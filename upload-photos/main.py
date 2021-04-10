import drive_source
import firebase_target
import crop_and_augment
from tqdm import tqdm
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
                f"{student_id}/register/{index}.jpg", './temp.jpg')


def save_augment_photos():
    all_files = firebase_instance.storage.list_files()
    for file_ in all_files:
        print(file_.name)
        # firebase_instance.download_image(file_.name, './augment.jpg')
        # result = face_instance.crop('./augment.jpg')
        # break


save_augment_photos()
