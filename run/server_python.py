import os
import cv2
import faiss
import pickle
import numpy as np
import faiss
from tqdm import tqdm
import json
from dateutil.tz import gettz

from __init__ import PYTHON_PATH
from utils.AIlibs import AILIBS
# Configuration networks, kafka
from utils.sever_config import config
mCONFIG = config()

from datetime import datetime

# import utils libs
mAILIBS = AILIBS

META = "lastMetaDataPath"
STUDENT = "student"
FEATURE = "feature"
TIMESTAMP = "timestamp"
NPY_PATH = "npy_path"
MIN_DIST = 60.15

VECTOR_FILE = "vector.index"
FEATURE_FILE = "features.pickle"
INDEX_FILE = "index.pickle"
THRESHOLD_FILE = "threshold.pickle"
FEATURE_NPY_FILE = "feature.npy"
CHECKIN_NPY_FILE = "checkin.npy"
METADATA_FILE = "metadata.json"
STUDENT_PATH_LIST = "student_path_list"
CREATED_AT = "created_at"
VECTOR_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", VECTOR_FILE)
FEATURE_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", FEATURE_FILE)
INDEX_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", INDEX_FILE)
FEATURE_NPY_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", FEATURE_NPY_FILE)
THRESHOLD_PATH = os.path.join(
    PYTHON_PATH, "ailibs_data", "data", THRESHOLD_FILE)
METADATA_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", METADATA_FILE)
CHECKIN_NPY_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", CHECKIN_NPY_FILE)



class Main():
    def __init__(self):
        pass

    def run(self):
        while True:
            data, flag = mCONFIG.schedule()
            if flag:
                faiss_flag = mCONFIG.check_faiss(data[META])
                if faiss_flag:
                    index = faiss.read_index(VECTOR_PATH)
                    with open(FEATURE_PATH, 'rb') as encodePickle:
                        feature_vector = pickle.load(encodePickle)
                    with open(INDEX_PATH, 'rb') as encodePickle:
                        y = pickle.load(encodePickle)
                else:
                    index = faiss.IndexFlatL2(128)
                    index.ntotal
                    feature_vector = []
                    y = []
                for FEATURE_FIREBASE in tqdm(data[STUDENT]):
                    userid = FEATURE_FIREBASE.split("/")[1]
                    mCONFIG.download_file(FEATURE_FIREBASE, FEATURE_NPY_PATH)
                    feature = np.load(FEATURE_NPY_PATH)
                    feature = feature.astype(np.float32)
                    index.add(feature)
                    feature_vector.append(feature)
                    y.append(userid)
                with open(METADATA_PATH) as json_file:
                    meta = json.load(json_file)
                timestamp = str(datetime.now(gettz("Asia/Ho_Chi_Minh")).strftime("%Y-%m-%d %H:%M:%S"))
                meta[STUDENT_PATH_LIST] += data[STUDENT]
                meta[CREATED_AT] = timestamp
                with open(METADATA_PATH, 'w') as outfile:
                    json.dump(meta, outfile)
                y_set = set(y)
                if len(y_set) == 1:
                    threshold = [MIN_DIST]*len(y)
                else:
                    threshold = mCONFIG.calculate_threshold(feature_vector, y)
                print(threshold)
                faiss.write_index(index, VECTOR_PATH)
                with open(INDEX_PATH, "wb") as handle:
                    pickle.dump(y, handle, protocol=pickle.HIGHEST_PROTOCOL)
                with open(FEATURE_PATH, "wb") as handle:
                    pickle.dump(feature_vector, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
                with open(THRESHOLD_PATH, "wb") as handle:
                    pickle.dump(threshold, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
                mCONFIG.send_data(timestamp, data[META],data)

            data, flag = mCONFIG.checkin()
            if flag:
                feature_vector = np.array(data[FEATURE]).astype(np.float32)
                np.save(CHECKIN_NPY_PATH, feature_vector)
                mCONFIG.commit_checkin(data[TIMESTAMP], data[NPY_PATH],data)



if __name__ == '__main__':
    Main().run()
