import os
import faiss
import dlib
import cv2
import pickle
import glob


import __init__
from test import PYTHON_PATH

from utils.AIlibs import AILIBS

mAILIBS = AILIBS
data = {}

data_path = os.path.join("/home/hoangphuc/OneDrive/Documents/data/*")
feature_path = os.path.join(PYTHON_PATH, "test", "features.pickle")
if os.path.exists(feature_path):
    with open(feature_path, 'rb') as handle:
        data = pickle.load(handle)

for filename in glob.iglob(data_path):
    print(filename.split('/')[-1])
    if filename.split('/')[-1] not in data:
        data[filename.split('/')[-1]] = []
    for image_path in os.listdir(filename):
        if image_path != 'sample.jpg':
            if int(image_path.split('.')[0]) >= len(data[filename.split('/')[-1]]):
                input_path = os.path.join(filename, image_path)
                frame = cv2.imread(input_path)
                dets = mAILIBS.DETECTOR.detect(frame)
                for det in dets:
                    features = mAILIBS.EXTRACTOR.extract(frame, det)
                    data[filename.split('/')[-1]].append(features)

with open(feature_path,"wb") as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

            