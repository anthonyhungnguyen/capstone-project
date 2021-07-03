import os
import numpy
import pickle
import tensorflow as tf
import math
import faiss
from sklearn import metrics
import numpy as np

from ailibs.__init__ import timeit


class FaceClassifier():
    """
    This is implementation for dlib resnet, support classify face.

    """

    def __init__(self, **kwargs):
        """
        Constructor.
        Args:

        """
        try:
            self.log = kwargs.get('log', False)
            vector_path = kwargs.get('vector_faiss')
            y_path = kwargs.get('vector_index')
            threshold = kwargs.get('threshold')
            self.__index = faiss.read_index(vector_path)
            with open(y_path, 'rb') as encodePickle:
                self.__y = pickle.load(encodePickle)
            with open(threshold, 'rb') as encodePickle:
                self.__threshold = pickle.load(encodePickle)
        except Exception as e:
            print("Exception", e)

    def __classify(self, features):
        """
        Classify face features using loaded model.

        Args:
            image (numpy array): image contains objects.

        Returns:
            dist (list): minimum dist.
            identity (str): identity name 
        """
        identity_list = []
        for feature in features:
            similarities, neighbors = self.__index.search(feature, k=1)
            identity = {}
            identity["name"] = "Unknown"
            identity['dist'] = 1000

            # if similarities[0][0] < MIN_DIST:
            if similarities[0][0] < self.__threshold[neighbors[0][0]]:
                identity['name'] = self.__y[neighbors[0][0]]
                identity['dist'] = similarities[0][0]
            elif identity['name'] == "Unknown":
                identity['dist'] = similarities[0][0]
            identity_list.append(identity)

        return identity_list

    def classify(self, features):
        """
        Classify face features.
        Args:
            features (array): face features.

        Returns:
            results (list): list of detected objects [x, y, w, h] in image.
        """ 

        return self.classify_list([features])[0]

    @timeit
    def classify_list(self, features_list):
        """
        Classify list of face features.
        Args:
            image (numpy array): image contains objects.

        Returns:
            results (list): list of class name and score.
        """
        results = []
        identity_list = self.__classify(features_list)
        results = []
        for identity in identity_list:
            info = {'name': identity['name'], 'score': identity['dist']}
            results.append(info)

        return results

    def update(self, vector_faiss, vector_index, thres_path):
        self.__index = faiss.read_index(vector_faiss)
        with open(vector_index, 'rb') as encodePickle:
            self.__y = pickle.load(encodePickle)
        with open(thres_path, 'rb') as encodePickle:
            self.__threshold = pickle.load(encodePickle)