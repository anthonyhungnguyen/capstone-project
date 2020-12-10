import os
import numpy
import pickle
import tensorflow as tf
import math
from sklearn import metrics


from ailibs.__init__ import timeit

SCORE_THESHOLD = 90
AUTO_SCORE_THRESHOLD = 70


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

            classname_path = kwargs.get('classname')
            model_path = kwargs.get('model')
            auto_model_path = kwargs.get('auto_models')
            self.__score_threshold = kwargs.get('score_threshold', SCORE_THESHOLD)
            self.__auto_score_threshold = kwargs.get(
                'auto_score_threshold', AUTO_SCORE_THRESHOLD)
            self.log = kwargs.get('log', False)

            self.__classname = None
            self.__session = None
            self.__model = None
            self.__data = None
            self.__auto_models = dict()

            with open(os.path.join(classname_path), 'rb') as handle:
                data = pickle.load(handle)
            self.__classname = data['code']
            self.__classname.sort()
            self.__data = data

            self.__model = tf.keras.models.load_model(model_path)
            for model_name in os.listdir(auto_model_path):
                self.__auto_models[model_name[:-3]
                                ] = tf.keras.models.load_model(f'{auto_model_path}/{model_name}')

        except Exception as e:
            print("Exception", e)

    def check_load_success(self):
        if self.__model == None:
            return False
        else:
            return True

    def __classify(self, features):
        """
        Classify face features using loaded model.

        Args:
            image (numpy array): image contains objects.

        Returns:
            scores_list (list): list of scores.
        """
        scores_list = self.__model.predict(features)

        return scores_list

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
        scores_list = self.__classify(updated_list)

        # post processing
        results = []
        for scores, face in zip(scores_list, faces_list):
            info = self.post_processing(scores, face)
            results.append(info)
        return results

    def probability(self, A, B, x):
        return 1/(math.exp(A + B*x) + 1)

    def post_processing(self, scores, face, filter=True):
        """
        Format classifier results to class name, score.
        Args:
            results (array): confidence core of calss name list

        Returns:
            name (str): name of features
            score (float): confidence of features
        """
        info = {}
        scores = scores.flatten()
        score = round(scores[scores.argmax()] * 100, 3)
        print("Name: ", self.__classname[scores.argmax()], "; Score: ", score)
        if filter == True and score >= self.__score_threshold:
            name = self.__classname[scores.argmax()]
            pred = self.__auto_models[name].predict(face)
            root_mse = numpy.sqrt(metrics.mean_squared_error(pred, face))
            encoder_prob = self.probability(
                self.__data[name]['A'], self.__data[name]['B'], root_mse)
            print("Name: ", name, "; Score: ", encoder_prob * 100)
            if encoder_prob * 100 > self.__auto_score_threshold:
                info = {
                    'name': name,
                    'score': score
                }
            else:
                info = {
                    'name': "Unknown",
                    'score': 1 - encoder_prob
                }
        else:
            info = {
                'name': "Unknown",
                'score': 0.99
            }
        return info