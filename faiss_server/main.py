from flask import Flask, request, jsonify
import json
import faiss
import pickle
import time
import numpy as np


app = Flask(__name__)

with open('../model/threshold.pickle', 'rb') as thP:
    threshold = pickle.load(thP)
index = faiss.read_index('../model/ip.index')


@app.route('/indexing', methods=['POST'])
def face_detect():
    if request.method == 'POST':
        data = np.array(request.json, dtype=np.float32)
        start = time.time()
        similarities, neighbors = index.search(data, k=10)
        end = time.time()
        print("Searching time: ", end - start)
        similarities = similarities.flatten()
        neighbors = neighbors.flatten()
        if similarities[0] < threshold[neighbors[0]] / 2 + 20:
            return jsonify({'neighbors': str(neighbors[0])})
        return jsonify({'neighbors': None})


# When debug = True, code is reloaded on the fly while saved
app.run(host='0.0.0.0', port='5000', debug=True)
