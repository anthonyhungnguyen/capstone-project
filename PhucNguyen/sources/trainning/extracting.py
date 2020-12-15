import os
import sys
import cv2
import dlib
import numpy as np
import pickle
import pandas as pd
import json
from imutils import paths
from datetime import datetime
from time import time

import django
from __init__ import PYTHON_PATH
os.environ['DJANGO_SETTINGS_MODULE'] = 'checkin.settings'
django.setup()


from django.conf import settings
from checkin.facecheckin.models import Configuration

# import ailibs libraries
from ailibs.detector.dlib.FaceDetector import FaceDetector
from ailibs.extractor.dlib.FaceExtractor import FaceExtractor
from utils.Status import TRAINING_STATUS

from utils.LogFCI import setup_logger
LOG_TRAINNING_PATH = getattr(settings, 'LOG_TRAINNING_PATH')
LOGGER = setup_logger('training', LOG_TRAINNING_PATH)


LOG_TIME = False
data_path = os.path.join(PYTHON_PATH, "ailibs_data")
shape_predictor_path = os.path.join(
    data_path, "extractor", "dlib", "shape_predictor_68_face_landmarks.dat")
face_recognition_path = os.path.join(
    data_path, "extractor", "dlib", "dlib_face_recognition_resnet_model_v1.dat")

FACE_DETECTOR = FaceDetector(log=LOG_TIME)
FACE_EXTRACTOR = FaceExtractor(
    shape_predictor=shape_predictor_path, face_recognition=face_recognition_path, log=LOG_TIME)


def extract_features():
    """
    Extract 128D vector features for the case of using those features for trainning not evaluating
    """
    Configuration.objects.filter(key="training_status").update(value=TRAINING_STATUS.IN_PROCESSING)
    LOGGER.info('1. Update training_status = {}.'.format(TRAINING_STATUS.IN_PROCESSING))
    db_path = os.path.join(os.path.dirname(PYTHON_PATH), 'storage')

    start_time = str(datetime.now())
    dbfaces_path = os.path.join(db_path, "dbfaces")
    dbfeatures_path = os.path.join(db_path, "dbfeatures")
    with open(f"{dbfaces_path}/data.json") as json_file:
        augmentclass = json.load(json_file)
    image_list = list(sorted(augmentclass.keys()))

    index_list = [int(i) for i in sorted(os.listdir(dbfeatures_path))]
    datasets = {}
    unknown_data = {}
    unknown_data['Unknown'] = []
    counts = {}
    update = {}
    classname = {}
    for user_id in augmentclass.keys():
        if user_id != 'Unknown':
            datasets[user_id] = {}
            counts[user_id] = 0
            update[user_id] = False

    if len(index_list) != 0:
        index = str(index_list[-1]) if len(index_list) > 0 else str(0)
        features_root_path = os.path.join(dbfeatures_path, index)
        features_path = os.path.join(features_root_path, "features.pickle")
        classname_path = os.path.join(features_root_path, "classname.pickle")
        unknown_path = os.path.join(features_root_path, "unknown.pickle")

        LOGGER.info('features_path = {}.'.format(features_path))
        with open(features_path, 'rb') as handle:
            data = pickle.load(handle)
        LOGGER.info('classname_path = {}.'.format(classname_path))
        with open(classname_path, 'rb') as handle:
            classname = pickle.load(handle)
        LOGGER.info('unknown_path = {}.'.format(unknown_path))
        with open(unknown_path, 'rb') as handle:
            unknown = pickle.load(handle)

        unknown_data = unknown
        for user_id in data:
            datasets[user_id] = data[user_id]
            counts[user_id] = classname['counts'][user_id]

    for user_id in image_list:
        if user_id == 'Unknown' and len(unknown_data['Unknown']) != 0:
            continue
        LOGGER.info('user_id = {}.'.format(user_id))
        user_images_path = os.path.join(dbfaces_path, user_id)
        user_images_list = list(paths.list_images(user_images_path))
        for (i, img) in enumerate(user_images_list):
            id = img.split('/')[-1].split('.')[-2]
            if (user_id in datasets and id in datasets[user_id]):
                continue

            update[user_id] = True
            LOGGER.info('{}: Extracting {}/{}'.format(user_id, i, len(user_images_list)))
            img = dlib.load_rgb_image(img)
            dets = FACE_DETECTOR.detect(img)

            for det in dets:
                features = FACE_EXTRACTOR.extract(img, det)
                features = np.array(features).reshape(1, 128)

                if np.isnan(features).any():
                    continue
                if user_id != 'Unknown':
                    counts[user_id] += 1
                    datasets[user_id][id] = features
                else:
                    unknown_data['Unknown'].append(features)
    # Save features
    print(unknown_data['Unknown'])
    dbfeatures_path = os.path.join(db_path, "dbfeatures")
    index_list = [int(i) for i in sorted(os.listdir(dbfeatures_path))]
    index = str(index_list[-1] + 1) if len(index_list) > 0 else str(0)
    save_path = os.path.join(dbfeatures_path, index)

    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    features_path = os.path.join(save_path, "features.pickle")
    classname_path = os.path.join(save_path, "classname.pickle")
    unknown_path = os.path.join(save_path, "unknown.pickle")

    with open(features_path, 'wb') as handle:
        pickle.dump(datasets, handle, protocol=pickle.HIGHEST_PROTOCOL)
        LOGGER.info('Saved {}.'.format(features_path))

    classname['update'] = update
    classname['code'] = list(datasets.keys())
    classname['counts'] = counts
    classname['start_time'] = start_time
    classname['end_time'] = str(datetime.now())
    with open(classname_path, 'wb') as handle:
        pickle.dump(classname, handle, protocol=pickle.HIGHEST_PROTOCOL)
        LOGGER.info('Saved {}.'.format(classname_path))

    LOGGER.info('Classname: {}.'.format(classname))

    with open(unknown_path, 'wb') as handle:
        pickle.dump(unknown_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        LOGGER.info('Saved {}.'.format(unknown_path))

    del datasets
    del unknown_data

    LOGGER.info('Done extracting data.')

def extract():
    try:
        LOGGER.info('I. EXTRACTING...')
        extract_features()
    except Exception as e:
        LOGGER.error('Exception {}.'.format(e))
        LOGGER.error("%s", str(e))
# if __name__ == "__main__":

#     Configuration.objects.filter(key="training_status").update(value=TRAINING_STATUS.IN_PROCESSING)
#     db_path = os.path.join(os.path.dirname(PYTHON_PATH), 'storage')
    # extract_features(db_path)
