import cv2

cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)

while True:
    ret, frame = cam.read()
    cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("frame",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    frame = cv2.flip(frame,1)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

cv2.destroyAllWindows()
