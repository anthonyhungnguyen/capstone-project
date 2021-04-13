from __init__ import PYTHON_PATH
from utils import firebase_target
from utils import drive_source
import uuid
from tqdm import tqdm
import face_request
import os


FACE_SERVER = "http://localhost:5000"

drive_instance = drive_source.Drive()
firebase_instance = firebase_target.FireBase()
face_instance = face_request.FaceRequest(FACE_SERVER)
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
                f"student/{student_id}/register/photos/{index}.jpg", './temp.jpg', str(uuid.uuid4()))


def save_crop_and_augment_photos():
    all_files = firebase_instance.get_all_register_urls()
    track_list = []
    for file_ in tqdm(all_files):
        path_list = file_.split('/')
        student_id = path_list[1]
        if student_id in track_list:
            continue
        track_list.append(student_id)
        firebase_instance.download_image(file_, './raw.jpg')
        face_instance.crop('./raw.jpg')
        face_instance.augment('./crop.jpg')
        firebase_instance.put_image(
            f"student/{student_id}/augment/photos/0.jpg", './crop.jpg', str(uuid.uuid4()))
        for i in range(4):
            firebase_instance.put_image(
                f"student/{student_id}/augment/photos/0_{i}.jpg", f'./augment_{i}.jpg', str(uuid.uuid4()))


def save_features():
    all_files = firebase_instance.get_all_augment_urls()
    print(all_files)
    for file_ in tqdm(all_files):
        path_list = file_.split('/')
        full_path = '/'.join(path_list[:3])
        file_name = path_list[-1].split('.')[0]
        firebase_instance.download_image(file_, './feature.jpg')
        result = face_instance.feature('./feature.jpg')
        firebase_instance.put_txt(
            f"{full_path}/features/{file_name}.npy", './index.npy')


save_features()
