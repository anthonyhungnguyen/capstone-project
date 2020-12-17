from flask import Flask, request, jsonify
import json
import faiss
import pickle
import numpy as np


app = Flask(__name__)

index = faiss.read_index('../model/vector.index')


@app.route('/indexing', methods=['POST'])
def face_detect():
    if request.method == 'POST':
        data = np.array(request.json, dtype=np.float32)
        result = index.search(data, k=10)
        # return jsonify({'distance': result[0].tolist(), 'neighbors': result[1].tolist()})
        return json.dumps({'distance': result[0].tolist(), 'neighbors': result[1].tolist()})


# When debug = True, code is reloaded on the fly while saved
app.run(host='0.0.0.0', port='5000', debug=True)
