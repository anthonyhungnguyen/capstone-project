import tempfile
import cv2

fp = tempfile.TemporaryFile()
fp.seek(0)
print(fp.read())
# cv2.imwrite('Test.jpg', img)
