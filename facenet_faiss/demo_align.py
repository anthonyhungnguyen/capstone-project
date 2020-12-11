
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
identities = list(data.keys())

vector_dist = list(map(lambda x: list(zip([x[0]*len(x[1])], x[1])), data.items()))
vector_dist = [x for y in vector_dist for x in y ]
# print(vector_dist)
model = tf.keras.models.load_model('facenet_keras.h5')
model.load_weights('facenet_keras_weights.h5')

while True:
    ret, frame = cam.read()
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
        dist_list = list(map(lambda x: (x[0], 
                            np.linalg.norm(np.asarray(face) - np.asarray(x[1]))), vector_dist))
        dist_list.sort(key=lambda x: x[1])
        cv2.putText(frame, dist_list[0][0], (d.left(), d.top()), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

cv2.destroyAllWindows()