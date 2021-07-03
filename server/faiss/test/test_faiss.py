import os
import faiss
import dlib
import cv2
import pickle


import __init__
from test import PYTHON_PATH

from utils.AIlibs import AILIBS

mAILIBS = AILIBS

data_path = os.path.join(PYTHON_PATH, "ailibs_data")
STREAM_PATH = os.path.join(PYTHON_PATH, "test", "image", "test_khoaT.jpg")
feature_path = os.path.join(data_path, "classifier", "facenet", "features.pickle")

with open('test/index.pickle', 'rb') as encodePickle:
    y = pickle.load(encodePickle)
print(len(y))   
index = faiss.read_index("test/vector.index")

print("N:", index.ntotal)
print("D:", index.d)
print("values:", index.distances)


frame = cv2.imread(STREAM_PATH)
dets = mAILIBS.DETECTOR.detect(frame)
print(len(dets))
for det in dets:
    features = mAILIBS.EXTRACTOR.extract(frame, det)
    similarities, neighbors = index.search(features, k=1)
    print(similarities)
    print(neighbors)
    result = neighbors[0][0]
    print(y[result])
    print(similarities[0][0])
