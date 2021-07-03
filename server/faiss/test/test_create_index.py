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
feature_path = os.path.join(data_path, "classifier", "facenet", "features.pickle")


with open(feature_path, 'rb') as encodePickle:
    data = pickle.load(encodePickle)

y = []
X = []  
class_count = 0
index = faiss.read_index("test/vector.index")
print(index)
classnames = list(data.keys())
print(classnames)
for classname in classnames:
    y += [classname]*len(data[classname])
    class_count += 1
    for i in range(len(data[classname])):
        X.append(data[classname][i])
print(y)
print(X[0].shape)

index = faiss.IndexFlatL2(128)
index.ntotal

for x in X:
    index.add(x)
faiss.write_index(index, 'test/vector.index')

with open("test/index.pickle","wb") as handle:
    pickle.dump(y, handle, protocol=pickle.HIGHEST_PROTOCOL)
