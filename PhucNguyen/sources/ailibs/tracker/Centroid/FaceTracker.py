# import the necessary packages
import os
import cv2
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

from streaming import PYTHON_PATH
from ailibs.__init__ import timeit
from utils.alert import Alert

utils_path = os.path.join(PYTHON_PATH, "utils")
alert_image_path = os.path.join(utils_path, "mail_alert", "images")


ALERT = Alert(images=alert_image_path)
ACCEPT_MSG = "ACCEPT"


class FaceTracker():
    """
    This is implementation for tracking face.

    """

    def __init__(self, **kwargs):
        """
        Constructor.
        Args:

        """
        self.log = kwargs.get('log', False)
        # initialize the next unique object ID along with two ordered
        # dictionaries used to keep track of mapping a given object
        # ID to its centroid and number of consecutive frames it has
        # been marked as "disappeared", respectively
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()

        # store the number of maximum consecutive frames a given
        # object is allowed to be marked as "disappeared" until we
        # need to deregister the object from tracking
        self.maxDisappeared = kwargs.get('maxDisappeared', 20)

        # alert images storage
        self.alert_path = kwargs.get('images')

        # send alert mail 1 time:
        self.flag = {}

    def register(self, centroid):
        """ add new ID by centroid. 

        Args:
            centroid (OrderedDict()): an order dict() of centroid point
        """

        # When registering an object we use the next available object
        # ID to store the centroid
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        """ remove ID by objectID. 

        Args:
            objectID (int): ID of object
        """

        # To deregister an object ID we delete the object ID from
        # both of our respective dictionaries
        del self.objects[objectID]
        del self.disappeared[objectID]

    @timeit
    def update(self, rects):
        """ update dictionary of object by rects. 

        Args:
            rects (dlib.rectangles): dlib rectangles from face detector

        Returns:
            OrderedDict(): dict of ID and its centroid
        """

        # Check to see if the list of input bounding box rectangles
        # is empty
        if len(rects) == 0:
            # loop over any existing tracked objects and mark them
            # as disappeared
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1

                # if we have reached a maximum number of consecutive
                # frames where a given object has been marked as
                # missing, deregister it
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)

            # return early as there are no centroids or tracking info
            # to update
            return self.objects

        # initialize an array of input centroids for the current frame
        inputCentroids = np.zeros((len(rects), 2), dtype="int")

        # loop over the bounding box rectangles
        # for (i, d) in enumerate(rects):
        # use the bounding box coordinates to derive the centroid
        for (i, rect) in enumerate(rects):
            startX = rect.left()
            endX = rect.right()
            startY = rect.bottom()
            endY = rect.top()
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        # if we are currently not tracking any objects take the input
        # centroids and register each of them
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i])

        # otherwise, are are currently tracking objects so we need to
        # try to match the input centroids to existing object
        # centroids
        else:
            # grab the set of object IDs and corresponding centroids
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())

            # compute the distance between each pair of object
            # centroids and input centroids, respectively -- our
            # goal will be to match an input centroid to an existing
            # object centroid
            D = dist.cdist(np.array(objectCentroids), inputCentroids)

            # in order to perform this matching we must (1) find the
            # smallest value in each row and then (2) sort the row
            # indexes based on their minimum values so that the row
            # with the smallest value as at the *front* of the index
            # list
            rows = D.min(axis=1).argsort()

            # next, we perform a similar process on the columns by
            # finding the smallest value in each column and then
            # sorting using the previously computed row index list
            cols = D.argmin(axis=1)[rows]

            # in order to determine if we need to update, register,
            # or deregister an object we need to keep track of which
            # of the rows and column indexes we have already examined
            usedRows = set()
            usedCols = set()

            # loop over the combination of the (row, column) index
            # tuples
            for (row, col) in zip(rows, cols):
                # if we have already examined either the row or
                # column value before, ignore it
                # val
                if row in usedRows or col in usedCols:
                    continue

                # otherwise, grab the object ID for the current row,
                # set its new centroid, and reset the disappeared
                # counter
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                # self.usernames[objectID] = ID[col]
                self.disappeared[objectID] = 0

                # indicate that we have examined each of the row and
                # column indexes, respectively
                usedRows.add(row)
                usedCols.add(col)

            # compute both the row and column index we have NOT yet
            # examined
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            # in the event that the number of object centroids is
            # equal or greater than the number of input centroids
            # we need to check and see if some of these objects have
            # potentially disappeared
            if D.shape[0] >= D.shape[1]:
                # loop over the unused row indexes
                for row in unusedRows:
                    # grab the object ID for the corresponding row
                    # index and increment the disappeared counter
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1

                    # check to see if the number of consecutive
                    # frames the object has been marked "disappeared"
                    # for warrants deregistering the object
                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)

            # otherwise, if the number of input centroids is greater
            # than the number of existing object centroids we need to
            # register each new input centroid as a trackable object
            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])

        # return the set of trackable objects
        return self.objects

    def check(self, d, NAME_LIST, ID):
        """ check if face is verified, that face will not be recognized again

        Args:
            d (dlib rectangle): face detector rectangle
            NAME_LIST (dict): user info
            ID (dict): Tracker ID

        Returns:
            bool: True if face will be recognized, otherwise.
        """
        for (faceID, centroid) in self.objects.items():
            [startX, endX, startY, endY] = [
                d.left(), d.right(), d.bottom(), d.top()]
            [cX, cY] = [int((startX + endX) / 2.0), int((startY + endY) / 2.0)]
            if cX - centroid[0] == 0 and cY - centroid[1] == 0:
                if faceID in ID.keys():
                    if ID[faceID] in NAME_LIST.keys():
                        if ACCEPT_MSG in NAME_LIST[ID[faceID]]['name']:
                            return False
        return True

    def exist(self, user, ID):
        """Check tracked face deregister or not

        Args:
            user (dict): user info
            ID (dict): tracker ID

        Returns:
            bool: True if tracked face still exist, otherwise.
        """
        for (faceID, centroid) in self.objects.items():
            if faceID in ID.keys():
                if ID[faceID] in user['name']:
                    return True
        return False

    def track_face(self, ID, trackcount, dets, user_list, NAME_LIST, line_track, FACE_TRACKING, frame):
        """Track face to verified the recognizition, send alert if unknown existed.

        Args:
            ID (dict): tracker ID
            trackcount (dict):  verified score of face
            dets (dlib rectangles): face detector rectangles
            user_list (dict): recognized users each time
            NAME_LIST (dict): check-in users
            line_track (dict): route of tracked face
            FACE_TRACKING (bool): flag of skip tracking
            frame (cv2): frame

        Returns:
            ID (dict): tracker ID
            trackcount (dict):  verified score of face
            line_track (dict): route of tracked face
            FACE_TRACKING (bool): flag of skip tracking
        """

        # update centroid tracker using the computed set of bounding
        # box rectangles
        for (faceID, centroid) in self.objects.items():
            face_utils = zip(dets, user_list)
            for i, face_util in enumerate(face_utils):
                # loop over the tracked objects
                # draw both the ID of the faces and the centroid of the
                # object on the output frame
                # centroid = centroid[0]
                d, NAME = face_util
                name = NAME['name']
                [startX, endX, startY, endY] = [
                    d.left(), d.right(), d.bottom(), d.top()]
                [cX, cY] = [int((startX + endX) / 2.0),
                            int((startY + endY) / 2.0)]

                if cX - centroid[0] == 0 and cY - centroid[1] == 0:
                    if faceID not in ID.keys():
                        ID[faceID] = "Unknown"
                        trackcount[faceID] = 0
                        self.flag[faceID] = True
                        line_track[faceID] = [centroid]
                    if FACE_TRACKING:
                        if (ID[faceID] != name):
                            trackcount[faceID] -= 1
                        if (ID[faceID] == name):
                            trackcount[faceID] += 1
                        if (trackcount[faceID] < 0):
                            ID[faceID] = name
                            trackcount[faceID] = 0
                        if ID[faceID] not in NAME_LIST:
                            continue
                        self.flag, NAME_LIST = ALERT.alert(
                            trackcount, ID, NAME_LIST, self.flag, faceID, frame)
            if faceID in line_track.keys():
                line_track[faceID].append(centroid)
