import dlib
import numpy
import pandas

from ailibs.__init__ import timeit


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
        self.__shape_predictor = dlib.shape_predictor(kwargs.get('shape_predictor'))
        self.__extractor = dlib.face_recognition_model_v1(kwargs.get('face_recognition'))

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
        features = self.__extractor.compute_face_descriptor(image, shape)
        features = numpy.asarray(features)
        features = pandas.DataFrame(features)
        return features