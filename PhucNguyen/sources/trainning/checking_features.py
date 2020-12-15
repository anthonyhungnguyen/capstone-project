import os
import pickle

from __init__ import PYTHON_PATH


def checking_features():
    dbfeatures_path = os.path.join(os.path.dirname(PYTHON_PATH), "storage", "dbfeatures")

    index_list = [int(i) for i in sorted(os.listdir(dbfeatures_path))]
    index = str(index_list[-1]) if len(index_list) > 0 else str(0)
    save_path = os.path.join(dbfeatures_path, index)


    features_path = os.path.join(save_path, "features.pickle")
    print(features_path)
    with open(features_path, 'rb') as handle:
        features = pickle.load(handle)

    print(features.keys())
    print(features['PhucNguyen'])

    classname = {}
    classname_path = os.path.join(save_path, "classname.pickle")
    with open(classname_path, 'rb') as handle:
        classname = pickle.load(handle)

    print(classname_path)
    print(classname.keys())

    print(classname['code'])
    print(classname['start_time'])
    print(classname['end_time'])

    unknown_path = os.path.join(save_path, "unknown.pickle")
    with open(unknown_path, 'rb') as handle:
        unknown = pickle.load(handle)
    print(unknown.keys())

    # test_path = os.path.join(save_path, "test.pickle")
    # print(test_path)
    # with open(test_path, 'rb') as handle:
    #     test = pickle.load(handle)
    # for name, features in test.items():
    #     for feature in features:
    #         print(name, " ", feature)
    # print(test.keys())
    
