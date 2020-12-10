import dlib
import cv2
import numpy as np

from ailibs.__init__ import timeit

FACE_TYPE = 2
FACE_NAME = "face"
FACE_SCORE = 1.0


class FaceDetector():
    """
    This is implementation for dlib face detector, support detect face.

    """

    def __init__(self, **kwargs):
        """
        Constructor.
        Args:

        """
        self.log = kwargs.get('log', False)
        self.__modelFile = kwargs.get('detector_model')
        self.__configFile = kwargs.get('detector_proto')
        self.__detector = cv2.dnn.readNetFromCaffe(
            self.__configFile, self.__modelFile)

    @timeit
    def detect(self, image):
        """
        Detect objects in given image using loaded model.
        Args:
            image (numpy array): image contains objects.

        Returns:
            results (list): list of detected objects [x, y, w, h] in image.
        """
        results = []
        h, w = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                     (300, 300), (104.0, 117.0, 123.0))
        self.__detector.setInput(blob)
        faces = self.__detector.forward()
        # to draw faces on image
        for i in range(faces.shape[2]):
            confidence = faces[0, 0, i, 2]
            if confidence > 0.99:
                box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x, y, x1, y1) = box.astype("int")
                rec = dlib.rectangle(x, y, x1, y1)
                results.append(rec)
        return results

    @staticmethod
    def get_position(det, scale=1.0):
        left = int(det.left()*scale)
        right = int(det.right()*scale)
        top = int(det.top()*scale)
        bottom = int(det.bottom()*scale)

        return [left, top, right, bottom]

    @staticmethod
    def post_processing(detects):
        """
        Update format of detected objects.
        Args:
            detects (objects): dlib rectangles

        Returns:
            results (list): list of detected objects [x, y, w, h] in image.
        """
        results = []
        for d in detects:
            left = d.left()
            top = d.top()
            width = d.right() - d.left()
            height = d.bottom() - d.top()
            obj = [FACE_TYPE, FACE_NAME, [left, top, width, height], FACE_SCORE]

            results.append(obj)
        return results
