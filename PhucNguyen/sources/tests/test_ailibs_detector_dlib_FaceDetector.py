# TBU

if __name__ == "__main__":
    import os
    import sys
    import cv2
    import dlib

    from __init__ import PYTHON_PATH
    print('PYTHON_PATH', PYTHON_PATH)

    from ailibs.detector.dlib.FaceDetector import FaceDetector

    path = os.path.join(PYTHON_PATH, "ailibs_data", "testing", "images", "faces.jpg")
    LOG_TIME = True

    image = cv2.imread(path)
    print(path, image.shape)

    detector = FaceDetector(log=False)

    dets = detector.detect(image)
    print(dets, type(dets))
    features_list = []
    for d in dets:
        [left, top, right, bottom] = FaceDetector.get_position(d)
        print([left, top, right, bottom])