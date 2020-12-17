import os
import cv2
import numpy as np
from __init__ import PYTHON_PATH
from ailibs.detector.dnn.FaceDetector import FaceDetector
from ailibs.tracker.Kalman.FaceTracker import FaceTracker

dnn_path = os.path.join(PYTHON_PATH, "ailibs_data/detector/dnn")

proto_path = os.path.join(dnn_path, "deploy.prototxt")
model_path = os.path.join(dnn_path,"res10_300x300_ssd_iter_140000.caffemodel")

LOG=True
DETECTOR = FaceDetector(detector_proto=proto_path,detector_model=model_path,log=LOG)
TRACKER = FaceTracker(log=LOG)
camera = cv2.VideoCapture(0)

line_track = {}


while True:
    ret, frame = camera.read()
    dets = DETECTOR.detect(frame)
    trackerfaces=None
    flag=False
    for det in dets:
        [l, t, r, b] = DETECTOR.get_position(det)
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 255), 2)
        face = np.array([[l, t, r, b]])
        if flag == False:
            trackerfaces = face
            flag = True
        else:
            trackerfaces = np.concatenate([trackerfaces, face])
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 255), 2)
    if flag == True:
        trackers = TRACKER(trackerfaces)

        for tracker in trackers:
            [startX, endY, endX, startY] = tracker[:-1]
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            faceID = int(tracker[-1])
            if faceID not in line_track:
                line_track[faceID] = []
            line_track[faceID] += [(cX, cY)]

            text = "ID {}".format(faceID)
            cv2.putText(frame, text, (int(startX), int(endY)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        for tracker in trackers:
            if faceID in line_track.keys():
                centroid_trackors = line_track[faceID]
                for i, c in enumerate(centroid_trackors):
                    if i == 0:
                        end_point = (c[0], c[1])
                    else:
                        start_point = end_point
                        end_point = (c[0], c[1])
                        cv2.line(frame, start_point, end_point, (255, 150, 0), 1)

    cv2.imshow("dnn_frame", frame)
    k = cv2.waitKey(60) & 0xff
    if k == 27:
        break

camera.release()
cv2.destroyAllWindows()