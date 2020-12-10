# import os
# import sys
import cv2
# import dlib
# from __init__ import PYTH ON_PATH
# print('PYTHON_PATH', PYTHON_PATH)
# from ailibs.tracker.Kalman.FaceTracker import FaceTracker
# from ailibs.tracker.Centroid.FaceTracker import FaceTracker
# from ailibs.detector.dlib.FaceDetector import FaceDetector
# from ailibs.detector.dnn.FaceDetector import FaceDetector
# LOG_TIME = True
# data_path = os.path.join(PYTHON_PATH, "ailibs_data")
# dnn_proto = os.path.join(data_path, "detector","dnn","deploy.prototxt")
# dnn_model = os.path.join(data_path, "detector","dnn","res10_300x300_ssd_iter_140000.caffemodel")


if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    # DECTECTOR = FaceDetector(log=LOG_TIME)
    # DECTECTOR = FaceDetector(detector_model=dnn_model, detector_proto=dnn_proto,log=LOG_TIME)
    # TRACKER = FaceTracker()
    while True:
        success, frame = camera.read()

        # dets = DECTECTOR.detect(frame)
        
        # features_list = []
        # for d in dets:
        #     [left, top, right, bottom] = FaceDetector.get_position(d)
        #     print("Dets: ", [left, top, right, bottom])
        #     trackparam = [left, top, right, bottom, 1]
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)
        # face_trackers = TRACKER(dets)
        # print("TRACKER: ",face_trackers)

        # for (faceID, centroid) in face_trackers.items():
        #     text = "ID {}".format(faceID)
        #     cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
        #         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #     cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()