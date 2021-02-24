import os
import numpy
import pickle
import tensorflow as tf
import math
from sklearn import metrics

from ailibs.__init__ import timeit

MIN_DIST = 60.15


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
            feature_path = kwargs.get('feature')

            with open(os.path.join(feature_path), 'rb') as handle:
                data = pickle.load(handle)
            self.__data = data.items()
            self.__classname = list(data.keys())

            self.__vector_dist = list(
                map(lambda x: list(zip([x[0]]*len(x[1]), x[1])), data.items()))
            self.__vector_dist = [x for y in self.__vector_dist for x in y]
            self.log = kwargs.get('log', False)

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
            identity = {}
            identity["name"] = "Unknown"
            identity['dist'] = 1000
            dist_list = list(map(lambda x: (x[0], numpy.sum(
                numpy.square(numpy.asarray(feature) - numpy.asarray(x[1])))), self.__vector_dist))

            dist_list.sort(key=lambda x: x[1])
            # print(dist_list[0][1])
            if dist_list[0][1] < MIN_DIST:
                identity['name'] = dist_list[0][0]
                identity['dist'] = dist_list[0][1]
            elif identity['name'] == "Unknown":
                identity['dist'] = dist_list[0][1]
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

        # # post processing
        # results = []
        # for scores, face in zip(scores_list, faces_list):
        #     info = self.post_processing(scores, face)
        #     results.append(info)
        return results

    # def probability(self, A, B, x):
    #     return 1/(math.exp(A + B*x) + 1)

    # def post_processing(self, scores, face, filter=True):
    #     """
    #     Format classifier results to class name, score.
    #     Args:
    #         results (array): confidence core of calss name list

    #     Returns:
    #         name (str): name of features
    #         score (float): confidence of features
    #     """
    #     info = {}
    #     scores = scores.flatten()
    #     score = round(scores[scores.argmax()] * 100, 3)
    #     print("Name: ", self.__classname[scores.argmax()], "; Score: ", score)
    #     if filter == True and score >= self.__score_threshold:
    #         name = self.__classname[scores.argmax()]
    #         pred = self.__auto_models[name].predict(face)
    #         root_mse = numpy.sqrt(metrics.mean_squared_error(pred, face))
    #         encoder_prob = self.probability(
    #             self.__data[name]['A'], self.__data[name]['B'], root_mse)
    #         print("Name: ", name, "; Score: ", encoder_prob * 100)
    #         if encoder_prob * 100 > self.__auto_score_threshold:
    #             info = {
    #                 'name': name,
    #                 'score': score
    #             }
    #         else:
    #             info = {
    #                 'name': "Unknown",
    #                 'score': 1 - encoder_prob
    #             }
    #     else:
    #         info = {
    #             'name': "Unknown",
    #             'score': 0.99
    #         }
    #     return info
