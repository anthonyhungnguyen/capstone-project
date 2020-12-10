# import the necessary packages
import os
import cv2
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

from streaming import PYTHON_PATH
from ailibs.__init__ import timeit
from utils.alert import Alert

from utils.associate_detection_trackers import associate_detections_to_trackers
from filterpy.kalman import KalmanFilter


utils_path = os.path.join(PYTHON_PATH, "utils")
alert_image_path = os.path.join(utils_path, "mail_alert", "images")


ALERT = Alert(images=alert_image_path)
ACCEPT_MSG = "ACCEPT"

class KalmanTracker(object):
    counter = 1
    def __init__(self, dets):
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array([[1,0,0,0,1,0,0],
                              [0,1,0,0,0,1,0],
                              [0,0,1,0,0,0,1],
                              [0,0,0,1,0,0,0],  
                              [0,0,0,0,1,0,0],
                              [0,0,0,0,0,1,0],
                              [0,0,0,0,0,0,1]])
        self.kf.H = np.array([[1,0,0,0,0,0,0],
                              [0,1,0,0,0,0,0],
                              [0,0,1,0,0,0,0],
                              [0,0,0,1,0,0,0]])
        self.kf.R[2:,2:] *= 10.
        self.kf.P[4:,4:] *= 100.
        self.kf.P *= 10.
        self.kf.Q[-1,-1] *= 0.01
        self.kf.Q[4:,4:] *= 0.01
        self.kf.x[:4] = np.array([dets[0], dets[1], dets[2], dets[3]]).reshape((4, 1))
        self.id = KalmanTracker.counter
        # self.kf.alpha = 100
        KalmanTracker.counter += 1
    
    def __call__(self):
        if((self.kf.x[6]+self.kf.x[2])<=0):
            self.kf.x[6] *= 0.0
        self.kf.predict()
        return self.kf.x
    
    def correction(self, measurement):
        self.kf.update(measurement)

    def get_current_x(self):
        bbox = (np.array([self.kf.x[0], self.kf.x[1], self.kf.x[2], self.kf.x[3]]).reshape((1, 4)))
        return bbox

class FaceTracker():
    """
    This is implementation for tracking face.

    """

    # def __init__(self):
    def __init__(self, **kwargs):
        self.log = kwargs.get('log', False)
        self.current_trackers = []

    def __call__(self, detections):
        print("Inside FaceTracker: ", detections)
        retain_trackers = []

        if len(self.current_trackers) == 0:
            self.current_trackers = []
            for d in range(len(detections)):
                tracker = KalmanTracker(detections[d])
                measurement = np.array((4,1), np.float32)
                measurement = np.array([[int(detections[d, 0])], [int(detections[d, 1])], [int(detections[d, 2])],
                                        [int(detections[d, 3])]], np.float32)
                tracker.correction(measurement)
                self.current_trackers.append(tracker)
            
            for trk in self.current_trackers:
                d = trk.get_current_x()
                retain_trackers.append(np.concatenate((d[0], [trk.id])).reshape(1,-1))

            if(len(retain_trackers) > 0):
                return np.concatenate(retain_trackers)
        
            return np.empty((0,5))
        
        else:
            predicted_trackers = []
            for t in range(len(self.current_trackers)):
                predictions = self.current_trackers[t]()[:4]
                predicted_trackers.append(predictions)

            predicted_trackers = np.asarray(predicted_trackers)

            matched, unmatched_detections, unmatched_trackers = associate_detections_to_trackers(detections, 
                                                                                                predicted_trackers)
            
            print ('Matched Detections & Trackers', len(matched))
            print ('Unmatched Detections', len(unmatched_detections))
            print ('Unmatched Trackers', len(unmatched_trackers))
            print ('Current Trackers', len(self.current_trackers))

            for t in range(len(self.current_trackers)):
                if(t not in unmatched_trackers):
                    d = matched[np.where(matched[:,1]==t)[0], 0]
                    self.current_trackers[t].correction(np.array([detections[d, 0], detections[d, 1], 
                    detections[d, 2], detections[d, 3]]).reshape((4, 1)))

            for i in unmatched_detections:
                tracker = KalmanTracker(detections[i])
                measurement = np.array((4,1), np.float32)
                measurement = np.array([[int(detections[i, 0])], [int(detections[i, 1])], [int(detections[i, 2])],
                                        [int(detections[i, 3])]], np.float32)
                tracker.correction(measurement)
                self.current_trackers.append(tracker)

            for index in sorted(unmatched_trackers, reverse=True):
                del self.current_trackers[index]
            
            for trk in self.current_trackers:
                d = trk.get_current_x()
                retain_trackers.append(np.concatenate((d[0], [trk.id])).reshape(1,-1))

        if(len(retain_trackers) > 0):
            return np.concatenate(retain_trackers)

        return np.empty((0,5))
