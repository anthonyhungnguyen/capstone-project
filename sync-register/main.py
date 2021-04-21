from __init__ import PYTHON_PATH
from utils import firebase_target
from utils import drive_source
import uuid
from tqdm import tqdm
import face_request
import os
import datetime
import json
import requests
import pandas as pd
import requests

FACE_SERVER = "http://localhost:5000"

drive_instance = drive_source.Drive()
firebase_instance = firebase_target.FireBase()
face_instance = face_request.FaceRequest(FACE_SERVER)
drive = drive_instance.authorize_drive()


def find_differences_drive_firebase():
    all_student_folders = drive_instance.load_all_folders_files(
        drive, drive_instance.ROOT_ID)
    all_firebase_paths = firebase_instance.get_all_register_urls()
    drive_raw = []
    firebase_raw = []
    drive_id = []
    for folder_ in tqdm(all_student_folders):
        student_id = folder_['title']
        student_files = drive_instance.load_all_folders_files(
            drive, folder_['id'])
        for index, file_ in enumerate(student_files):
            drive_raw.append(f'{student_id}_{index}.jpg')
            drive_id.append(file_)
    for file_ in tqdm(all_firebase_paths):
        path_list = file_.split('/')
        student_id = path_list[1]
        filename = path_list[-1]
        firebase_raw.append(f'{student_id}_{filename}')
    differences = list(set(drive_raw) - set(firebase_raw))
    for d in differences:
        file_ = drive_id[drive_raw.index(d)]
        path_list = d.split('_')
        student_id = path_list[0]
        index = path_list[1]
        drive_instance.save_image_by_id(drive, file_['id'], 'temp.jpg')
        firebase_instance.put_image(
            f"student/{student_id}/register/photos/{index}", './temp.jpg', str(uuid.uuid4()))


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
    for file_ in tqdm(all_files):
        path_list = file_.split('/')
        full_path = '/'.join(path_list[:3])
        file_name = path_list[-1].split('.')[0]
        firebase_instance.download_image(file_, './feature.jpg')
        result = face_instance.feature('./feature.jpg')
        firebase_instance.put_txt(
            f"{full_path}/features/{file_name}.npy", './index.npy')


def init_class():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    firebase_instance.put_txt(
        f'/subject/201_CO0000_CC01/{current_date}/metadata.json', 'subject.json')
    all_features = firebase_instance.get_all_augment_features()
    json.dump({
        "student_path_list": [],
        "created_at": current_date
    }, open("subject.json", "w"))


def init_students():
    all_students = firebase_instance.get_all_student_ids()
    json_students = [{'id': student, 'password': ''}
                     for student in all_students]
    json_subjects = [{'user_id': student, 'subject_id': 'CO0000',
                      'group_code': 'CC01', 'semester': 201} for student in all_students]
    df = pd.DataFrame.from_records(json_students)
    df.to_csv('students_mysql.csv', index=False)

    df = pd.DataFrame.from_records(json_subjects)
    df.to_csv('subjects_mysql.csv', index=False)


def save_register_images():
    all_files = firebase_instance.get_all_register_urls()
    get_first_register_photo = [
        x for x in all_files if x.split('/')[-1] == '0.jpg']
    update_dict = {x.split('/')[1]: firebase_instance.get_url(x)
                   for x in get_first_register_photo}
    for student_id, image_link in tqdm(update_dict.items()):
        requests.post(f"http://localhost:8080/api/auth/{student_id}/upload_register_photo", {
            "imageLink": image_link
        })


def send_request():
    json = {
        "semester": 201,
        "groupCode": "CC01",
        "subjectID": "CO3025",
        "name": "System Design and Analysis",
        "studentList": [1614058,
                        1652595,
                        1712187,
                        1752015,
                        1752041,
                        1752044,
                        1752067,
                        1752089,
                        1752139,
                        1752169,
                        1752244,
                        1752255,
                        1752259,
                        1752290,
                        1752335,
                        1752394,
                        1752494,
                        1752516,
                        1752522,
                        1752567,
                        1752637,
                        2053234]
    }
    requests.post("http://localhost:8080/api/init/register_full", json=json)


send_request()
