import argparse
import os
from time import time
import dlib
import pickle
import requests


import cv2
import numpy as np
from __init__ import PYTHON_PATH
from utils.utils import Logger, mkdir
from ailibs.detector.dlib.FaceDetector import FaceDetector
from ailibs.tracker.Kalman2.FaceTracker import FaceTracker
from ailibs.extractor.facenet.FaceExtractor import FaceExtractor

url = "http://172.16.0.183:5000/indexing"
LOG=True
DETECTOR = FaceDetector(log=LOG)

margin = 15
detect_interval = 1
scale_rate = 1
data_path = os.path.join(PYTHON_PATH, "ailibs_data")
output_path = os.path.join(PYTHON_PATH,"tests/output")
shape_predictor_path = os.path.join(data_path, "extractor", "facenet", "shape_predictor_68_face_landmarks.dat")
extract_model_path = os.path.join(data_path, "extractor", "facenet", "facenet_keras.h5")
extract_model_weight_path = os.path.join(data_path, "extractor", "facenet", "weights.h5")
extract_labels_path = os.path.join(data_path, "extractor", "facenet", "encoded_faces_with_labels.pickle")
EXTRACTOR = FaceExtractor(shape_predictor=shape_predictor_path, model=extract_model_path, model_weight=extract_model_weight_path, log=LOG)

logger = Logger()

def main():
    global colours, img_size
    mkdir(output_path)
    # for display
    colours = np.random.rand(32, 3)

    # init tracker
    tracker = FaceTracker(max_age=50)  # create instance of the SORT tracker

    logger.info('Start track and extract......')
    
    video_name = 0
    directoryname = os.path.join(output_path, "vid")
    logger.info('Video_name:{}'.format(video_name))
    cam = cv2.VideoCapture(video_name)
    c = 0
    while True:
        final_faces = []
        addtional_attribute_list = []
        ret, frame = cam.read()
        if not ret:
            logger.warning("ret false")
            break
        if frame is None:
            logger.warning("frame drop")
            break

        # frame = cv2.resize(frame, (0, 0), fx=scale_rate, fy=scale_rate)
        # r_g_b_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if c % detect_interval == 0:
            img_size = np.asarray(frame.shape)[0:2]
            dets = DETECTOR.detect(frame)
            face_list = []
            for det in dets:
                [left, top, right, bottom] = DETECTOR.get_position(det)
                item = [left, top, right, bottom]
                
                face_list.append(item)
        final_faces = np.array(face_list)

        trackers = tracker.update(final_faces, img_size, directoryname, detect_interval)

        c += 1

        for d in trackers:
            d = d.astype(np.int32)
            cv2.rectangle(frame, (d[0], d[1]), (d[2], d[3]), colours[d[4] % 32, :] * 255, 3)
            if final_faces != []:
                cv2.putText(frame, 'ID : %d  DETECT' % (d[4]), (d[0] - 10, d[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.75,
                            colours[d[4] % 32, :] * 255, 2)
                cv2.putText(frame, 'DETECTOR', (5, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (1, 1, 1), 2)
            else:
                cv2.putText(frame, 'ID : %d' % (d[4]), (d[0] - 10, d[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75,
                            colours[d[4] % 32, :] * 255, 2)
            det = dlib.rectangle(int(d[0]), int(d[1]), int(d[2]), int(d[3]))
            features = EXTRACTOR.extract(frame,det)
            # print("FEATURES: ", type(features))
            # data = pickle.dumps(features, protocol=pickle.HIGHEST_PROTOCOL)
            resp_data = requests.post(url, json=features.tolist()).json()
            # if resp_data['distance']:
            #     distances = np.asarray(resp_data['distance'])
            #     neighbors = np.asarray(resp_data['neighbors'])
            #     id = y[np.bincount(np.squeeze(neighbors)).argmax()]
            #     cv2.putText(frame, identities[id], (d.left(), d.top()), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()