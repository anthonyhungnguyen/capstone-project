from flask import Flask, request
import json
import faiss
import pickle

app = Flask(__name__)

index  = faiss.read_index('vector.index')
@app.route('/indexing', methods=['POST'])
def face_detect():
    if request.method == 'POST':
        data = pickle.loads(request.data)
        result = index.search(data.reshape(1,-1), k=10)
        if result:
            # left, right, top, bottom, jaw, right_eye_brown, left_eye_brown, nose, nose_2, right_eye, left_eye, mouth, mouth_2 = result
            # print('Face', ret)
            # return json.dumps({'box':[left, right, top, bottom, jaw, right_eye_brown, left_eye_brown, nose, nose_2, right_eye, left_eye, mouth, mouth_2]})
            return json.dumps({'result': result})
        else:
            return json.dumps({'result': None})


# When debug = True, code is reloaded on the fly while saved
app.run(host='192.168.9.104', port='5001', debug=True)
