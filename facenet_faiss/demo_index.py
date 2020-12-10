
import dlib
import cv2
import pickle
import numpy as np
import tensorflow as tf
import requests
import pickle
url = "http://172.16.9.132:5001/indexing"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
model = tf.keras.models.load_model('facenet_keras.h5')
model.load_weights('weights.h5')
cam = cv2.VideoCapture(0)
cam.set(3, 400)
cam.set(4, 400)
INPUT_SIZE = 160
with open('encoded_faces_with_labels.pickle', 'rb') as handle:
    data = pickle.load(handle)

del data['code']
identities = list(data.keys())
y = None
for i, (key, values) in enumerate(data.items()):
  for value in values:
    if y is None:
      y = [i]
    else:
      y.append(i)
# model = tf.keras.models.load_model('facenet_keras.h5')
# model.load_weights('facenet_keras_weights.h5')

while True:
    ret, frame = cam.read()
    min_dist = float('inf')
    dets = detector(frame)
    for d in dets:
        shape = predictor(frame, d)
        face_frame = dlib.get_face_chip(frame, shape, size=INPUT_SIZE)
        face_frame = face_frame.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_frame.mean(), face_frame.std()
        face_frame = (face_frame - mean) / std
        cv2.imshow('face', face_frame)
        face_frame = face_frame[..., ::-1]
        face = model.predict(face_frame.reshape(1, INPUT_SIZE, INPUT_SIZE, 3))
        data = pickle.dumps(face, protocol=pickle.HIGHEST_PROTOCOL)
        resp_data = requests.post(url, data=data).json()
        if resp_data['distance']:
            distances = np.asarray(resp_data['distance'])
            neighbors = np.asarray(resp_data['neighbors'])
            id = y[np.bincount(np.squeeze(neighbors)).argmax()]
            cv2.putText(frame, identities[id], (d.left(), d.top()), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

cv2.destroyAllWindows()