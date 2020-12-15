import os
import pickle
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
from tensorflow.keras.optimizers import Adam
import shutil
from datetime import datetime

from __init__ import PYTHON_PATH

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'checkin.settings'
django.setup()

from utils.Status import TRAINING_STATUS
from checkin.facecheckin.models import Configuration

def extract_X_y(data):
    X = []
    y = []
    for name in data['code']:
        X.extend([i for i in data[name]])
        y.extend([name] * len(data[name]))
    return X, y


def encode_X_y(X, y, data):
    X = np.array(X)
    y = np.array(y)
    labelEncoder, oneHotEncoder = LabelEncoder(), OneHotEncoder()
    y = labelEncoder.fit_transform(y).reshape(-1, 1)
    y = oneHotEncoder.fit_transform(y).toarray().reshape(-1, 1, len(data['code']))

    return X, y


def train(db_path, face_classifier_path=None):
    start_time = str(datetime.now())
    dbfeatures_path = os.path.join(db_path, "dbfeatures")
    dbclassifiers_path = os.path.join(db_path, "dbclassifiers")

    index_list = [int(i) for i in sorted(os.listdir(dbfeatures_path))]
    index = str(index_list[-1]) if len(index_list) > 0 else str(0)
    features_root_path = os.path.join(dbfeatures_path, index)
    features_path = os.path.join(features_root_path, "features.pickle")
    classname_path = os.path.join(features_root_path, "classname.pickle")

    index_list = [int(i) for i in sorted(os.listdir(dbclassifiers_path))]
    index = str(index_list[-1] + 1) if len(index_list) > 0 else str(0)
    classifiers_path = os.path.join(dbclassifiers_path, index)
    if not os.path.isdir(classifiers_path):
        os.mkdir(classifiers_path)
    model_path = os.path.join(classifiers_path, "model.h5")

    data = None
    print("features_path", features_path)
    with open(features_path, 'rb') as handle:
        data = pickle.load(handle)

    X, y = extract_X_y(data)

    X, y = encode_X_y(X, y, data)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(X_train.shape)
    print(y.shape)
    model = Sequential([
        Dense(1024, input_shape=(1, 128), activation='relu'),
        Dense(len(data['code']), activation='softmax')
    ])

    model.compile(optimizer=Adam(),
                loss='categorical_crossentropy',
                metrics=['accuracy'])
    history = model.fit(X_train, y_train, epochs=50, validation_split=0.2)
    print(model.predict(X_train[0].reshape(-1, 1, 128)), y_train[0])
    print(history.history.keys())
    model.save(model_path)
    shutil.copy2(classname_path, classifiers_path)
    end_time = str(datetime.now())

    # copy to face classifier
    if face_classifier_path:
        shutil.copy2(classname_path, face_classifier_path)
        shutil.copy2(model_path, face_classifier_path)
    print("Done !!!", start_time, end_time)

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(PYTHON_PATH), 'storage')
    face_classifier_path = os.path.join(PYTHON_PATH, "ailibs_data", "classifier", "resnet")
    train(db_path, face_classifier_path)
    Configuration.objects.filter(key="training_status").update(value=TRAINING_STATUS.STOP)
