import os
import cv2

from __init__ import PYTHON_PATH
from ailibs.detector.dlib.FaceDetector import FaceDetector
from ailibs.extractor.facenet.FaceExtractor import FaceExtractor


data_path = os.path.join(PYTHON_PATH, "ailibs_data")
shape_predictor_path = os.path.join(
    data_path, "extractor", "dlib", "shape_predictor_68_face_landmarks.dat")
model_path = os.path.join(data_path, "extractor",
                          "facenet", "facenet_keras.h5")
weight_path = os.path.join(
    data_path, "extractor", "facenet", "weights.h5")


LOG_TIME = True


class AILIBS:
    DETECTOR = FaceDetector(log=LOG_TIME)
    EXTRACTOR = FaceExtractor(shape_predictor=shape_predictor_path,
                              model=model_path, model_weight=weight_path, log=LOG_TIME)

