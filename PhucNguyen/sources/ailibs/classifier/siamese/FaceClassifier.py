import os
import numpy
import pickle
import tensorflow as tf
import math
from sklearn import metrics

from ailibs.__init__ import timeit

MIN_DIST = 0.45


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
            print(data)
            self.__data = data
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
            min_dist = float('inf')
            print("FEATURE #####################: ",feature)
            for (name, encoded_image_names) in self.__data.items():
                # print(encoded_image_names)
                # distance between two embedding vector
                # print(encoded_image_name)
                for index, encoded_image_name in encoded_image_names.items():
                    dist = numpy.linalg.norm(numpy.asarray(feature) - numpy.asarray(encoded_image_name))
                    # print(name, dist)
                    if dist < min_dist:
                        min_dist = dist
                        identity = name
                if min_dist >= MIN_DIST:
                    identity = "Unknown"
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

        # convert features list to n-array (n, 1, 128)
        updated_list = []
        faces_list = []
        for features in features_list:
            face = numpy.array(features).reshape(1, 128)
            faces_list.append(face)
            features = numpy.asarray(features.transpose()).reshape(-1, 1, 128)
            updated_list.append(features)
        updated_list = numpy.concatenate(updated_list, axis=0)
        identity_list = self.__classify(updated_list)
        results = []
        for identity in identity_list:
            info = {'name': identity}
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