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
def create_user_path(newface_path):
    if not os.path.isdir(newface_path):
        os.mkdir(newface_path)
def register_user(frame, face_detector, face_extractor, user_id):

    status = False
    message = "OK"
    try:
        dbpath = "/opt/webapps/Phuc_FCI20200819/facecheckin/streaming/storage/dbfaces"
        padding = 10
        newface_path = os.path.join(dbpath, user_id)
        create_user_path(newface_path)

        dets = face_detector.detect(frame)

        # check if no face is detected
        if len(dets) == 0:
            message = "NO FACE is detected !!!"
            return status, message
        # check if mutil faces are detected
        if len(dets) > 1:
            message = "Too MANY FACES !!!"
            return status, message
        # check if show frontal face
        if not is_frontal_face(frame, dets[0], face_extractor):
            message = "Please show YOUR FRONTAL FACE !!!"
            return status, message
        # check if non-blurring face

        # check if low-brightness face

        left = dets[0].left()
        top = dets[0].top()
        right = dets[0].right()
        bottom = dets[0].bottom()
        face = frame[max(0,top-padding):min(bottom+padding, frame.shape[0]), max(0,left-padding):min(right+padding, frame.shape[1])]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255))
        image_name = os.path.join(newface_path, str(int(time() * 1000))+'.jpg')
        cv2.imwrite(image_name, face)
        status = True
        return status, message
    except Exception as e:
        print("Exception", e)
        message = str(e)
        return status, message