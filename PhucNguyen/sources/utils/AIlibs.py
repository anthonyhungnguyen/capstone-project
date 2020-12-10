import os
import cv2

from __init__ import PYTHON_PATH
from ailibs.classifier.resnet.FaceClassifier import FaceClassifier as FaceClassifierRS
from ailibs.classifier.siamese.FaceClassifier import FaceClassifier as FaceClassifierSM
from ailibs.extractor.dlib.FaceExtractor import FaceExtractor
from ailibs.detector.dlib.FaceDetector import FaceDetector
from ailibs.tracker.Centroid.FaceTracker import FaceTracker
from utils.Status import TRAINING_STATUS


data_path = os.path.join(PYTHON_PATH, "ailibs_data")
utils_path = os.path.join(PYTHON_PATH, "utils")
shape_predictor_path = os.path.join(
    data_path, "extractor", "dlib", "shape_predictor_68_face_landmarks.dat")
face_recognition_path = os.path.join(
    data_path, "extractor", "dlib", "dlib_face_recognition_resnet_model_v1.dat")
feature_path = os.path.join(
    data_path, "classifier", "resnet", "features.pickle")
classname_path = os.path.join(
    data_path, "classifier", "resnet", "classname.pickle")
model_path = os.path.join(data_path, "classifier", "resnet", "model.h5")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOT_FOUND_IMAGE = os.path.join(
    PYTHON_PATH, "ailibs_data", "testing", "images", "notfound.jpg")
auto_models_path = os.path.join(data_path, "classifier", "resnet", "autoencoders")
alert_image_path = os.path.join(utils_path, "mail_alert", "images")
test_face_path = os.path.join(
    PYTHON_PATH, "ailibs_data", "testing", "images", "extract_face.jpg")

LOG_TIME = True

class AILIBS:
    DETECTOR = FaceDetector(log=LOG_TIME)
    EXTRACTOR = FaceExtractor(
            shape_predictor=shape_predictor_path, face_recognition=face_recognition_path, log=LOG_TIME)
    CLASSIFIER = None
    TRACKERS = FaceTracker(images=alert_image_path, log=LOG_TIME)

    def load_model():
        try:
            image = cv2.imread(test_face_path)
            dets = AILIBS.DETECTOR.detect(image)
            features = AILIBS.EXTRACTOR.extract(image, dets[0])
            user_list = AILIBS.CLASSIFIER.classify_list([features])
            print("_______load_model", user_list)
            return True
        except Exception as e:
            return False

    def update(status):

        if status == TRAINING_STATUS.NONE:
            if AILIBS.DETECTOR is None:
                AILIBS.DETECTOR = FaceDetector(log=LOG_TIME)
            if AILIBS.EXTRACTOR is None:
                AILIBS.EXTRACTOR = FaceExtractor(
                    shape_predictor=shape_predictor_path, face_recognition=face_recognition_path, log=LOG_TIME)
            if AILIBS.CLASSIFIER is not None:
                del AILIBS.CLASSIFIER
                AILIBS.CLASSIFIER = None
            print("AILIBS.update()", "TRAINING_STATUS.NONE")

        if status == TRAINING_STATUS.STOP:
            if AILIBS.DETECTOR is None:
                AILIBS.DETECTOR = FaceDetector(log=LOG_TIME)
            if AILIBS.EXTRACTOR is None:
                AILIBS.EXTRACTOR = FaceExtractor(
                    shape_predictor=shape_predictor_path, face_recognition=face_recognition_path, log=LOG_TIME)
            if AILIBS.CLASSIFIER is None:
                AILIBS.CLASSIFIER = FaceClassifierRS(
                    classname=classname_path, model=model_path, auto_models=auto_models_path, log=LOG_TIME)
                # print("---------------LOAD CLASSIFIER ------------")
                # AILIBS.CLASSIFIER = FaceClassifierSM(feature=feature_path, log=LOG_TIME)
            print("AILIBS.update()", "TRAINING_STATUS.STOP")

        if status == TRAINING_STATUS.IN_PROCESSING:
            if AILIBS.DETECTOR is not None:
                del AILIBS.DETECTOR
                AILIBS.DETECTOR = None
            if AILIBS.EXTRACTOR is not None:
                del AILIBS.EXTRACTOR
                AILIBS.EXTRACTOR = None
            if AILIBS.CLASSIFIER is not None:
                del AILIBS.CLASSIFIER
                AILIBS.CLASSIFIER = None
            print("AILIBS.update()", "TRAINING_STATUS.IN_PROCESSING")