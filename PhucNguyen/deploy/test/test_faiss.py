import faiss
import dlib
import cv2

import __init__
from test import PYTHON_PATH

from utils.AIlibs import AILIBS

mAILIBS = AILIBS


STREAM_PATH = "/home/hoangphuc/OneDrive/Documents/deploy/test/image/test.jpg"


index = faiss.read_index("test/vector.index")
print(index)


cam = cv2.VideoCapture(STREAM_PATH)
ret, frame = cam.read()
dets = mAILIBS.DETECTOR.detect(frame)
for det in dets:
    features = mAILIBS.EXTRACTOR.extract(frame, det)
    similarities, neighbors = index.search(features, k=10)
    print(similarities)
    print(neighbors)
