import dlib
import numpy
import pandas
import tensorflow as tf

from ailibs.__init__ import timeit

INPUT_SIZE = 160


class FaceExtractor():
    """
    This is implementation for dlib face extractor, support extract face.

    """

    def __init__(self, **kwargs):
        """
        Constructor.
        Args:

        """
        self.log = kwargs.get('log', False)
        print("shape path: ", kwargs.get('shape_predictor'))
        self.__shape_predictor = dlib.shape_predictor(
            kwargs.get('shape_predictor'))
        print("model path: ", kwargs.get('model'))
        self.__extractor = tf.keras.models.load_model(kwargs.get('model'))
        print("weight path: ", kwargs.get('model_weight'))
        self.__extractor.load_weights(kwargs.get('model_weight'))

    def extract_shape(self, image, det):
        """
        Extract eyes.
        Args:

        """
        return self.__shape_predictor(image, det)

    @timeit
    def extract(self, image, det):
        """
        Extract objects in given image using loaded model.
        Args:
            image (numpy array): image contains objects.
            det (dlib rectangle): dlib rectangle object - face

        Returns:
            results (list): list of detected objects [x, y, w, h] in image.
        """
        features = []
        shape = self.__shape_predictor(image, det)
        face_frame = dlib.get_face_chip(image, shape, size=INPUT_SIZE)
        face_frame = face_frame.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_frame.mean(), face_frame.std()
        face_frame = (face_frame - mean) / std
        face_frame = face_frame[..., ::-1]
        features = self.__extractor.predict(
            face_frame.reshape(1, INPUT_SIZE, INPUT_SIZE, 3))
        return features

    def extract_without_det(self, face_frame):
        face_frame = face_frame.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_frame.mean(), face_frame.std()
        face_frame = (face_frame - mean) / std
        face_frame = face_frame[..., ::-1]
        return self.__extractor.predict(face_frame.reshape(1, INPUT_SIZE, INPUT_SIZE, 3))

    @staticmethod
    def get_face_chip(frame, shape, size=160):
        return dlib.get_face_chip(frame, shape, size)
