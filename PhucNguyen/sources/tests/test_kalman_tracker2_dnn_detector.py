import argparse
import os
from time import time

import cv2
import numpy as np
from __init__ import PYTHON_PATH
from utils.utils import Logger, mkdir
from ailibs.detector.dnn.FaceDetector import FaceDetector
from ailibs.tracker.Kalman2.FaceTracker import FaceTracker

dnn_path = os.path.join(PYTHON_PATH, "ailibs_data/detector/dnn")

proto_path = os.path.join(dnn_path, "deploy.prototxt")
model_path = os.path.join(dnn_path,"res10_300x300_ssd_iter_140000.caffemodel")

LOG=True
DETECTOR = FaceDetector(detector_proto=proto_path,detector_model=model_path,log=LOG)

margin = 15
detect_interval = 1
scale_rate = 1
output_path = os.path.join(PYTHON_PATH,"tests/output")

logger = Logger()

def main():
    global colours, img_size
    mkdir(output_path)
    # for display
    colours = np.random.rand(32, 3)

    # init tracker
    tracker = FaceTracker(max_age=100)  # create instance of the SORT tracker

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

        frame = cv2.resize(frame, (0, 0), fx=scale_rate, fy=scale_rate)
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

        
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()