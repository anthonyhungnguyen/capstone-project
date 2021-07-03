import os
import cv2
from __init__ import PYTHON_PATH
from ailibs.utilities.FaceUtilities import FaceUtilities as UTILS
mUTILS = UTILS
from utils.AIlibs import AILIBS
mAILIBS = AILIBS

# STREAM_PATH = "/home/hoangphuc/Documents/thesis/vid/WIN_20210420_11_49_20_Pro.mp4"
# STREAM_PATH = "/home/hoangphuc/Documents/thesis/vid/WIN_20210420_11_50_33_Pro.mp4"
# STREAM_PATH = "/home/hoangphuc/Documents/thesis/vid/WIN_20210420_11_51_00_Pro.mp4"
# STREAM_PATH = "/home/hoangphuc/Documents/thesis/vid/WIN_20210420_11_51_27_Pro.mp4"
STREAM_PATH = "/home/hoangphuc/OneDrive/Documents/thesis/vid/2021-04-22-115426.webm"
STORAGE = "/home/hoangphuc/OneDrive/Documents/thesis/images/1652595"

if not os.path.exists(STORAGE):
    os.mkdir(STORAGE)

cam = cv2.VideoCapture(STREAM_PATH)
count = 0

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame,1)
    dets = mAILIBS.DETECTOR.detect(frame)
    if count % 5 == 0:
        for det in dets:
            [l, t, r, b] = mAILIBS.DETECTOR.get_position(det)
            if mUTILS.is_frontal_face(frame, det, mAILIBS.EXTRACTOR):
                cv2.imwrite(os.path.join(STORAGE, f"{count//5}.jpg"), frame)
            cv2.rectangle(frame, (l, t), (r, b), (0, 255, 255), 2)  
            break
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == 27:
        break  # esc to quit
    if count == 100:
        break  # esc to quit
    count = count + 1

cv2.destroyAllWindows() 