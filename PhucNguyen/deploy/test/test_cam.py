import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

cv2.destroyAllWindows()
