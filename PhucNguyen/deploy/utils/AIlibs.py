import os
import cv2

from __init__ import PYTHON_PATH
from ailibs.detector.dlib.FaceDetector import FaceDetector
from ailibs.extractor.facenet.FaceExtractor import FaceExtractor
from ailibs.classifier.siamese.FaceClassifier import FaceClassifier
from utils.LogFCI import setup_logger


data_path = os.path.join(PYTHON_PATH, "ailibs_data")
utils_path = os.path.join(PYTHON_PATH, "utils")
shape_predictor_path = os.path.join(
    data_path, "extractor", "dlib", "shape_predictor_68_face_landmarks.dat")
feature_path = os.path.join(
    data_path, "classifier", "facenet", "features.pickle")
classname_path = os.path.join(
    data_path, "classifier", "facenet", "classname.pickle")
model_path = os.path.join(data_path, "extractor",
                          "facenet", "facenet_keras.h5")
weight_path = os.path.join(
    data_path, "extractor", "facenet", "weights.h5")
LOG_STREAMING_PATH = os.path.join(data_path, "log", "fci_streaming.log")


LOG_TIME = True


class AILIBS:
    DETECTOR = FaceDetector(log=LOG_TIME)
    EXTRACTOR = FaceExtractor(shape_predictor=shape_predictor_path,
                              model=model_path, model_weight=weight_path, log=LOG_TIME)
    CLASSIFIER = FaceClassifier(feature=feature_path, log=LOG_TIME)
    LOGGER = setup_logger('streaming', LOG_STREAMING_PATH)
