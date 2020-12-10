import sys
import dlib
import cv2
import numpy as np
from imutils import paths
import numpy as np
import os
import pickle
import pandas as pd
import tensorflow as tf



detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


INPUT_SIZE = 160
model = tf.keras.models.load_model('facenet_keras.h5')
model.load_weights('weights.h5')

dataset = {}
for name in os.listdir('dbfaces'):
    dataset[name] = []

imagePaths = list(paths.list_images('dbfaces'))
num_of_images = len(imagePaths)
for(i, data) in enumerate(imagePaths):
    print(data)
    print(f'Processing image {i}/{num_of_images}')
    label = data.split('\\')[-2]
    img = dlib.load_rgb_image(data)
    dets = detector(img)
    for d in dets:
        shape = predictor(img, d)
        temp = dlib.get_face_chip(img, shape, size=INPUT_SIZE)
        temp = temp.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = temp.mean(), temp.std()
        temp = (temp - mean) / std
        face = model.predict(temp.reshape(1, INPUT_SIZE, INPUT_SIZE, 3))
        dataset[label].append(face)

dataset['code'] = list(dataset.keys())
with open('encoded_faces_with_labels.pickle', 'wb') as handle:
    pickle.dump(dataset, handle, protocol=pickle.HIGHEST_PROTOCOL)