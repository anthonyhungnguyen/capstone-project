import os 
import cv2 
import faiss
import pickle
import numpy as np

from __init__ import PYTHON_PATH
# Configuration networks, kafka
from utils.sever_config import config 
mCONFIG = config()

# import utils libs
from utils.AIlibs import AILIBS
mAILIBS = AILIBS

USERID = "userId"
PHOTO = "photo"
NAME = "name"
FEATURE = "feature"

# VECTOR_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", "vector.index")
# INDEX_PATH = os.path.join(PYTHON_PATH,"ailibs_data", "data", "index.pickle")

VECTOR_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", "vector.pickle")
INDEX_PATH = os.path.join(PYTHON_PATH,"ailibs_data", "data", "index.npy")



class Main():
    def __init__(self):
        pass
    
    def run(self):
        while True:
            data, flag = mCONFIG.register()
            if flag:
                if os.path.exists(VECTOR_PATH) and os.path.exists(INDEX_PATH):
                    with open(VECTOR_PATH, 'rb') as encodePickle:
                        index = pickle.load(encodePickle)
                    y = np.load(INDEX_PATH)
                else:
                    index = []
                    y = np.array([]).astype('str')
                image = mCONFIG.decode(data[PHOTO])
                dets = mAILIBS.DETECTOR.detect(image)
                for d in dets:
                    features = mAILIBS.EXTRACTOR.extract(image, d)
                    index.append(features.tolist())
                    y = np.append(y, data[USERID])
                    break
                print(y)     
                with open(VECTOR_PATH,"wb") as handle:
                    pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)
                np.save(INDEX_PATH, y)
                mCONFIG.send_data(index, y.tolist())

            data, flag = mCONFIG.checkin()         
            if flag:
                with open(VECTOR_PATH, 'rb') as encodePickle:
                    index = pickle.load(encodePickle)
                y = np.load(INDEX_PATH)
    
                index.append(data[FEATURE])
                y = np.append(y, data[NAME])
                print(y)     
                with open(VECTOR_PATH,"wb") as handle:
                    pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)
                np.save(INDEX_PATH, y)
                mCONFIG.send_data(index, y.tolist())              


if __name__ == '__main__':
    Main().run()