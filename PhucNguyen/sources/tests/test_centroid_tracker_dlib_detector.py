import cv2
from __init__ import PYTHON_PATH
from ailibs.detector.dlib.FaceDetector import FaceDetector
from ailibs.tracker.Centroid.FaceTracker import FaceTracker

LOG=True
DETECTOR = FaceDetector(log=LOG)
TRACKER = FaceTracker(log=LOG)
camera = cv2.VideoCapture(0)

line_track = {}

while True:
    ret, frame = camera.read()
    dets = DETECTOR.detect(frame)
    face_trackers = TRACKER.update(dets)
    for det in dets:
        [l, t, r, b] = DETECTOR.get_position(det)
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 255), 2)
    for (faceID, centroid) in face_trackers.items():
        text = "ID {}".format(faceID)
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if faceID not in line_track:
            line_track[faceID] = []
        line_track[faceID] += [centroid]

    for (faceID, centroid) in face_trackers.items():
        if faceID in line_track.keys():
            centroid_trackors = line_track[faceID]
            for i, c in enumerate(centroid_trackors):
                if i == 0:
                    end_point = (c[0], c[1])
                else:
                    start_point = end_point
                    end_point = (c[0], c[1])
                    cv2.line(frame, start_point, end_point, (255, 150, 0), 1)
    cv2.imshow("dlib_frame", frame)
    k = cv2.waitKey(60) & 0xff
    if k == 27:
        break

camera.release()
cv2.destroyAllWindows()