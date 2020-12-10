
import dlib
import cv2
import pickle
import numpy as np
import tensorflow as tf
from face_align import FaceAligner, resize

INPUT_SIZE = 160
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
fa = FaceAligner(predictor, desiredFaceHeight=INPUT_SIZE, desiredFaceWidth=INPUT_SIZE)
model = tf.keras.models.load_model('facenet_keras.h5')
model.load_weights('weights.h5')
cam = cv2.VideoCapture(0)
cam.set(3, 400)
cam.set(4, 400)

with open('encoded_faces_with_labels1.pickle', 'rb') as handle:
    data = pickle.load(handle)

del data['code']


# model = tf.keras.models.load_model('facenet_keras.h5')
# model.load_weights('facenet_keras_weights.h5')

while True:
    ret, frame = cam.read()
    min_dist = float('inf')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dets = detector(frame)
    for d in dets:
        face_frame = fa.align(frame, gray, d)
        face_frame = face_frame.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_frame.mean(), face_frame.std()
        face_frame = (face_frame - mean) / std
        cv2.imshow('face', face_frame)
        face_frame = face_frame[..., ::-1]
        face = model.predict(face_frame.reshape(1, INPUT_SIZE, INPUT_SIZE, 3))
        for (name, encoded_image_names) in data.items():
            for encoded_image_name in encoded_image_names:
                # print(encoded_image_name.shape)
                dist = np.linalg.norm(np.asarray(face) - np.asarray(encoded_image_name))
                print(name, dist)
                if dist < min_dist:
                    min_dist = dist
                    identity = name
        # if min_dist < threshold:
        #     cv2.putText(frame, identity, (200, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        # else:
        #     cv2.putText(frame, 'Guest', (200, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        cv2.putText(frame, identity, (d.left(), d.top()), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

cv2.destroyAllWindows()