import os
import pickle
import json
import random
from sklearn import metrics
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

from django.conf import settings
from utils.Status import TRAINING_STATUS
from checkin.facecheckin.models import Configuration

from utils.LogFCI import setup_logger
LOG_TRAINNING_PATH = getattr(settings, 'LOG_TRAINNING_PATH')
LOGGER = setup_logger('training', LOG_TRAINNING_PATH)


def extract_X_y(data):
    X = []
    y = []
    for name in list(data.keys()):
        X.extend([i for i in data[name].values()])
        y.extend([name] * len(data[name]))
    return X, y


def encode_X_y(X, y, data):
    X = np.array(X)
    y = np.array(y)
    labelEncoder, oneHotEncoder = LabelEncoder(), OneHotEncoder()
    y = labelEncoder.fit_transform(y).reshape(-1, 1)
    y = oneHotEncoder.fit_transform(
        y).toarray().reshape(-1, 1, len(list(data.keys())))

    return X, y


def outliers_removed(array):
    array = np.array(array)
    Q1 = np.quantile(array, 0.25)
    Q3 = np.quantile(array, 0.75)
    IQR = Q3 - Q1
    array = array[np.where((array >= (Q1 - 1.5*IQR)) &
                           (array <= (Q3 + 1.5*IQR)))]
    return list(array)


def train_all():

    db_path = os.path.join(os.path.dirname(PYTHON_PATH), 'storage')
    ailibs_data_path = os.path.join(
        PYTHON_PATH, "ailibs_data", "classifier", "resnet")


    dbfeatures_path = os.path.join(db_path, "dbfeatures")
    dbclassifiers_path = os.path.join(db_path, "dbclassifiers")

    index_list = [int(i) for i in sorted(os.listdir(dbfeatures_path))]
    index = str(index_list[-1]) if len(index_list) > 0 else str(0)
    features_root_path = os.path.join(dbfeatures_path, index)
    features_path = os.path.join(features_root_path, "features.pickle")
    classname_path = os.path.join(features_root_path, "classname.pickle")

    data = None
    print("features_path", features_path)
    LOGGER.info('features_path = {}.'.format(features_path))
    with open(features_path, 'rb') as handle:
        data = pickle.load(handle)
    LOGGER.info('classname_path = {}.'.format(classname_path))
    with open(classname_path, 'rb') as handle:
        classname = pickle.load(handle)

    # Call Resnet model:
    index_list = [int(i) for i in sorted(os.listdir(
        dbclassifiers_path)) if i != "dbautoencoders"]
    index = str(index_list[-1] + 1) if len(index_list) > 0 else str(0)
    classifiers_path = os.path.join(dbclassifiers_path, index)
    if not os.path.isdir(classifiers_path):
        os.mkdir(classifiers_path)
    model_path = os.path.join(classifiers_path, "model.h5")

    # receive model after training
    model = train_resnet_model(data)
    
    model.save(model_path)
    LOGGER.info('1. Done training {}.'.format(model_path))

    if ailibs_data_path:
        shutil.copy2(model_path, ailibs_data_path)

    # Call Encoders models:
    dbautoencoders_path = os.path.join(
        classifiers_path, "dbautoencoders")
    if not os.path.isdir(dbautoencoders_path):
        os.mkdir(dbautoencoders_path)
    unknown_path = os.path.join(features_root_path, "unknown.pickle")
    LOGGER.info('unknown_path = {}.'.format(unknown_path))
    with open(unknown_path, 'rb') as handle:
        unknown_data = pickle.load(handle)
    unknown = np.array(unknown_data["Unknown"])

    # index_list = [int(i) for i in sorted(os.listdir(dbautoencoders_path))]
    # index = str(index_list[-1] + 1) if len(index_list) > 0 else str(0)
    # autoencoders_path = os.path.join(dbautoencoders_path, index)
    # if not os.path.isdir(autoencoders_path):
    #     os.mkdir(autoencoders_path)

    # old_aucoder_path = os.path.join(features_root_path, "dbautoencoders")
    save_autoencoders_path = os.path.join(ailibs_data_path, "autoencoders")
    if not os.path.isdir(save_autoencoders_path):
        os.mkdir(save_autoencoders_path)
    encoder_list = os.listdir(dbautoencoders_path)
    for encode in encoder_list:
        encode_path = os.path.join(dbautoencoders_path, encode)
        shutil.copy2(autoencoders_model_path, save_autoencoders_path)

    # Receive models and classname after training and post-proccessing
    classname, encoders_models = train_encoder_model(data, unknown, classname)

    for person in encoders_models:
        autoencoders_model_path = os.path.join(
            dbautoencoders_path, person + '.h5')
        encoders_models[person].save(autoencoders_model_path)
        LOGGER.info('Saved {}.'.format(person))

    LOGGER.info('2. Done training {}.'.format(autoencoders_model_path))

    with open(classname_path, 'wb') as handle:
        pickle.dump(classname, handle, protocol=pickle.HIGHEST_PROTOCOL)
        LOGGER.info('classname_path = {}.'.format(classname_path))
    # copy to face classifier
    # save_autoencoders_path = os.path.join(
    #     ailibs_data_path, "autoencoders")
    # if not os.path.isdir(save_autoencoders_path):
    #     os.mkdir(save_autoencoders_path)
    if ailibs_data_path:
        shutil.copy2(classname_path, ailibs_data_path)

        # copy autoencoder
        for model in os.listdir(dbautoencoders_path):
            autoencoders_model_path = os.path.join(
                dbautoencoders_path, model)
            shutil.copy2(autoencoders_model_path, save_autoencoders_path)
    LOGGER.info('3. Update to {}.'.format(ailibs_data_path))

    Configuration.objects.filter(key="training_status").update(value=TRAINING_STATUS.STOP)
    LOGGER.info('4. Update training_status = {}.'.format(TRAINING_STATUS.STOP))

    del model
    del encoders_models

def train_resnet_model(data):
    # Model for classification:
    # After extracting features with Resnet, we pass them to Fully Connected Layer
    # for classification.
    start_time = str(datetime.now())

    X, y = extract_X_y(data)

    X, y = encode_X_y(X, y, data)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    LOGGER.info('X_train.shape = {}.'.format(X_train.shape))
    LOGGER.info('y.shape = {}.'.format(y.shape))

    model = Sequential([
        Dense(1024, input_shape=(1, 128), activation='relu'),
        Dense(len(list(data.keys())), activation='softmax')
    ])

    model.compile(optimizer=Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    history = model.fit(X_train, y_train, epochs=50, validation_split=0.2)
    # print(model.predict(X_train[0].reshape(-1, 1, 128)), y_train[0])
    LOGGER.info('history.history.keys() = {}.'.format(history.history.keys()))

    end_time = str(datetime.now())
    LOGGER.info('start_time = {}; end_time = .'.format(start_time, end_time))

    return model


def train_encoder_model(data, unknown, classname):
    # Auto Encoders models for anomaly detection, corporating with open set problem
    start_time = str(datetime.now())

    encoders_models = {}
    for person in list(data.keys()):
        LOGGER.info('person = {}.'.format(person))

        if classname['update'][person]:
            LOGGER.info('Update person = {}.'.format(person))
            X = list(data[person].values())

            X = np.array(X)

            X_train, X_test = train_test_split(
                X, test_size=0.2, random_state=42)

            model = Sequential()
            model.add(Dense(128, input_shape=(1, 128), activation='relu'))
            model.add(Dense(16, activation='relu'))
            model.add(Dense(128, activation='relu'))
            model.add(Dense(128))
            model.compile(loss='mean_squared_error',
                          optimizer='adam', run_eagerly=True)
            model.fit(X_train, X_train, verbose=1, epochs=100)

            encoders_models[person] = model
            classname[person] = encoders_post_proccessing(
                model, unknown, X_test)

    end_time = str(datetime.now())

    return classname, encoders_models


def encoders_post_proccessing(model, unknown, X_test):
    # Post-proccessing after training calculates necessary coeficients
    person_scorelist = []
    unknown_scorelist = []
    # get max value of person score
    for face in X_test:
        pred = model.predict(face)
        res = np.sqrt(metrics.mean_squared_error(pred, face))
        person_scorelist.append(res)
    person_scorelist = outliers_removed(person_scorelist)
    person_score = max(person_scorelist)
    LOGGER.info('Person score = {}.'.format(person_score))

    # get min value of unknown score
    for face in unknown:
        pred = model.predict(face)
        res = np.sqrt(metrics.mean_squared_error(pred, face))
        unknown_scorelist.append(res)
    unknown_scorelist = outliers_removed(unknown_scorelist)
    unknown_score = max(unknown_scorelist)
    LOGGER.info('Unknown score = {}.'.format(unknown_score))

    # compute parameters alpha, beta for auto encoder threshold
    B = 9.12/(unknown_score-person_score)
    A = -4.56 - B*person_score
    weight = {}
    weight["A"] = A
    weight["B"] = B

    return weight

def train ():
    try:
        LOGGER.info('II. TRAINING...')
        train_all()
    except Exception as e:
        LOGGER.error('Exception {}.'.format(e))
        LOGGER.error("%s", str(e))
# if __name__ == "__main__":
#     db_path = os.path.join(os.path.dirname(PYTHON_PATH), 'storage')
#     ailibs_data_path = os.path.join(
#         PYTHON_PATH, "ailibs_data", "classifier", "resnet")
#     train(db_path, ailibs_data_path)
#     Configuration.objects.filter(key="training_status").update(value=TRAINING_STATUS.STOP)
#     # import subprocess
#     # command = "bash {}/streaming/streaming.sh".format(PYTHON_PATH)
#     # subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
