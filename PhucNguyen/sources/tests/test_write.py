from __init__ import PYTHON_PATH
import dlib
import cv2
import os
from time import time
path = os.path.join(PYTHON_PATH, "ailibs_data",
                    "testing", "images", "faces.jpg")
path_ram = os.path.join(PYTHON_PATH, "ailibs_data",
                        "streaming")

for i in range(10):
    start = time()
    img = cv2.imread(path)
    end = time()
    print("Read cv2: ", end-start)

for i in range(10):
    start = time()
    cv2.imwrite("test_nor.jpg", img)
    end = time()
    print("Write normal: ", end-start)

for i in range(10):
    start = time()
    cv2.imwrite(os.path.join(path_ram, "test.jpg"), img)
    end = time()
    print("Write tempfile: ", end-start)

for i in range(10):
    start = time()
    img = cv2.imread(os.path.join(path_ram, "test.jpg"))
    end = time()
    print("Read tempfile: ", end-start)
