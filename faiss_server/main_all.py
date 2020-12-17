from flask import Flask, request, jsonify
import json
import faiss
import pickle
import requests
import numpy as np
import dlib
import tensorflow as tf

app = Flask(__name__)
# Load
with open('../model/mappingNameToId.json') as mappingFile:
    mappingNameToId = json.load(mappingFile)

index = faiss.read_index('../model/vector.index')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    '../model/shape_predictor_68_face_landmarks.dat')
model = tf.keras.models.load_model('../model/model.h5')
model.load_weights('../model/weights.h5')
INPUT_SIZE = 160


with open('../model/encoded_faces_with_labels.pickle', 'rb') as handle:
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


@app.route('/indexing', methods=['POST'])
def face_detect():
    def processDet(frame, d):
        shape = predictor(frame, d)
        face_frame = dlib.get_face_chip(frame, shape, size=INPUT_SIZE)
        face_frame = face_frame.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_frame.mean(), face_frame.std()
        face_frame = (face_frame - mean) / std
        face_frame = face_frame[..., ::-1]
        face = model.predict(face_frame.reshape(
            1, INPUT_SIZE, INPUT_SIZE, 3))
        return face

    def processFrame(frame):
        result = []
        dets = detector(frame)
        for d in dets:
            result.append(processDet(frame, d))
        return result

    if request.method == 'POST':
        frame = np.array(request.json, dtype=np.uint8)
        data = processFrame(frame)
        total = []
        for r in data:
            result = index.search(r, k=10)
            distances = result[0].tolist()
            neighbors = result[1].tolist()
            id = y[np.bincount(np.squeeze(neighbors)).argmax()]

            if (identities[id] in mappingNameToId):
                att_res = requests.post(f'http://localhost:8090/api/check/{mappingNameToId[identities[id]]}', json={
                    "id": "CO3021",
                    "groupCode": "CC01",
                    "semester": 201
                })
                print(att_res.text)
                total.append(att_res.text)
            else:
                print("unknown")
                total.append("Unknown")
        return json.dumps({"data": total})


# When debug = True, code is reloaded on the fly while saved
app.run(host='0.0.0.0', port='5000', debug=True)
