from __init__ import PYTHON_PATH
import cv2
from ailibs.utilities.FaceUtilities import FaceUtilities as UTILS
mUTILS = UTILS
from utils.AIlibs import AILIBS
mAILIBS = AILIBS

cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame,1)
    dets = mAILIBS.DETECTOR.detect(frame)
    for det in dets:
        [l, t, r, b] = mAILIBS.DETECTOR.get_position(det)
        if mUTILS.is_frontal_face(frame, det, mAILIBS.EXTRACTOR):
            cv2.putText(frame, "Yes", (l - 10, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else: 
            cv2.putText(frame, "No", (l - 10, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 255), 2)  
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

cv2.destroyAllWindows()