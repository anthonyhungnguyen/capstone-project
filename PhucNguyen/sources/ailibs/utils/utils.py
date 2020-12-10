import os
from time import time
import cv2
from imutils import face_utils
from scipy.spatial import distance as dist

left_jaw = 0
mid_jaw = 8
right_jaw = 16
mid_nose = 34
FACE_REGISTERING_COUNT = 0
FACE_REGISTERING_TOTAL = 100

def is_frontal_face(image, det, face_extractor):
    """
    Check ratio of face.
    Args:
        TBU
    Return:
        TBU
    """
    shape = face_extractor.extract_shape(image, det)
    shape = face_utils.shape_to_np(shape)
    nose2leftjaw = dist.euclidean(shape[mid_nose], shape[left_jaw])
    nose2midjaw = dist.euclidean(shape[mid_nose], shape[mid_jaw])
    nose2rightjaw = dist.euclidean(shape[mid_nose], shape[right_jaw])

    if False:
        print("left_jaw", nose2leftjaw, 'mid_jaw', nose2midjaw, 'right_jaw', nose2rightjaw)
        cv2.line(image, (shape[mid_nose][0],shape[mid_nose][1]) , (shape[left_jaw][0],shape[left_jaw][1]), (0, 255, 0), thickness=1)
        cv2.line(image, (shape[mid_nose][0],shape[mid_nose][1]) , (shape[mid_jaw][0],shape[mid_jaw][1]), (0, 255, 0), thickness=1)
        cv2.line(image, (shape[mid_nose][0],shape[mid_nose][1]) , (shape[right_jaw][0],shape[right_jaw][1]), (0, 255, 0), thickness=1)

        frame = cv2.putText(image, str(int(nose2leftjaw)), (shape[left_jaw][0]+5, shape[left_jaw][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
        frame = cv2.putText(image, str(int(nose2midjaw)), (shape[mid_jaw][0], shape[mid_jaw][1]-15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
        frame = cv2.putText(image, str(int(nose2rightjaw)), (shape[right_jaw][0]-30, shape[right_jaw][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

    minlf = min(nose2leftjaw, nose2rightjaw)
    if abs(nose2leftjaw - nose2rightjaw) < 1/2*minlf:
        if abs(minlf - nose2midjaw) < 1/2*min(minlf, nose2rightjaw):
            return True
        else:
            return False
    else:
        return False

def normalize_frame(frame, nw=640, nh=480):
    """
    Normalize image size
    Args:
        frame (int): input frame
        nw (int): normalized width
        nh (int): normalized height
    Returns:
        nframe (int): normalized frame
    """
    [fh, fw, channel] = frame.shape

    pw = int((fw-nw)/2)
    ph = int((fh-nh)/2)
    nframe = frame[ph:ph+nh, pw:pw+nw].copy()
    return nframe