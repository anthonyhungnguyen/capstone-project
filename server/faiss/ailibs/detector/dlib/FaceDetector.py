import dlib

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
        self.__detector = dlib.get_frontal_face_detector()

    @timeit
    def detect(self, image):
        """
        Detect objects in given image using loaded model.
        Args:
            image (numpy array): image contains objects.

        Returns:
            results (list): list of detected objects [x, y, w, h] in image.
        """
        results = self.__detector(image)
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
