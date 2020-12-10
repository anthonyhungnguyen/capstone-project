import os
import sys
import cv2
import dlib
import json
import numpy as np
from __init__ import PYTHON_PATH
from ailibs.detector.dnn.FaceDetector import FaceDetector
data_path = os.path.join(PYTHON_PATH, "ailibs_data")
face_detector_model_path = os.path.join(
    data_path, "detector", "dnn", "res10_300x300_ssd_iter_140000.caffemodel")
face_detector_proto_path = os.path.join(
    data_path, "detector", "dnn", "deploy.prototxt")


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(PYTHON_PATH), 'storage')
    dbfaces_path = os.path.join(db_path, "dbfaces")
    print(dbfaces_path)
    # detector = FaceDetector(log=False)
    detector = FaceDetector(detector_model=face_detector_model_path,
                                detector_proto=face_detector_proto_path, log=False)
    if os.path.isfile("log.json") is False:  
        data = {}
        data['PhucNguyen'] = False
        data['HungNguyen'] = False
        data['KhoaTran'] = False
        data['HungLe'] = False
        data['ChauTran'] = False
        data['HoangLu'] = False
        data['MaiPham'] = False
        data['TriNguyen'] = False
        data['ThongNguyen'] = False
        data['KhoaBui'] = False
        data['DucNguyen'] = False
        data['DatDoan'] = False
        data['Unknown'] = False
        with open(f"{dbfaces_path}/data.json", 'w') as outfile:
            json.dump(data, outfile)
    with open(f"{dbfaces_path}/data.json") as json_file:
        augmentclass = json.load(json_file)
    for user_id in augmentclass.keys():
        if augmentclass[user_id] == False and user_id != "Unknown":
            count = 0
            image = cv2.imread(f"{dbfaces_path}/{user_id}/sample.jpg")
            # dets = detector.detect(image)  
            # for det in dets:
            #     [left, top, right, bottom] = detector.get_position(det)
            #     face = image[top:bottom, left:right]
            for i in range(-21,0,3):
                rimg = rotate_image(image,i)
                dets = detector.detect(rimg) 
                for det in dets:
                    [left, top, right, bottom] = detector.get_position(det)
                    face = rimg[top:bottom, left:right]
                cv2.imwrite(f"{dbfaces_path}/{user_id}/{count}.jpg",face)
                count += 1
                for li in range(0,100,5):
                    limg = increase_brightness(face,li)
                    cv2.imwrite(f"{dbfaces_path}/{user_id}/{count}.jpg",limg)
                    count += 1

            for i in range(0,21,3):
                rimg = rotate_image(image,i)
                dets = detector.detect(rimg) 
                for det in dets:
                    [left, top, right, bottom] = detector.get_position(det)
                    face = rimg[top:bottom, left:right]
                cv2.imwrite(f"{dbfaces_path}/{user_id}/{count}.jpg",face)
                count += 1
                for li in range(0,100,5):
                    limg = increase_brightness(face,li)
                    cv2.imwrite(f"{dbfaces_path}/{user_id}/{count}.jpg",limg)
                    count += 1

            imageflip = cv2.flip(image,1)
            for i in range(-21,0,3):
                rimg = rotate_image(imageflip,i)
                dets = detector.detect(rimg) 
                for det in dets:
                    [left, top, right, bottom] = detector.get_position(det)
                    face = rimg[top:bottom, left:right]
                cv2.imwrite(f"{dbfaces_path}/{user_id}/{count}.jpg",face)
                count += 1
                for li in range(0,100,5):
                    limg = increase_brightness(face,li)
                    cv2.imwrite(f"{dbfaces_path}/{user_id}/{count}.jpg",limg)
                    count += 1

            for i in range(0,21,3):
                rimg = rotate_image(imageflip,i)
                dets = detector.detect(rimg) 
                for det in dets:
                    [left, top, right, bottom] = detector.get_position(det)
                    face = rimg[top:bottom, left:right]
                cv2.imwrite(f"{dbfaces_path}/{user_id}/{count}.jpg",face)
                count += 1
                for li in range(0,100,5):
                    limg = increase_brightness(face,li)
                    cv2.imwrite(f"{dbfaces_path}/{user_id}/{count}.jpg",limg)
                    count += 1            