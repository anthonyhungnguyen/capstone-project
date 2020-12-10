# TBU

if __name__ == "__main__":
    import os
    import sys
    import cv2
    import dlib

    from __init__ import PYTHON_PATH
    print('PYTHON_PATH', PYTHON_PATH)

    from ailibs.detector.dlib.FaceDetector import FaceDetector
    from ailibs.extractor.dlib.FaceExtractor import FaceExtractor
    from ailibs.classifier.siamese.FaceClassifier import FaceClassifier

    path = os.path.join(PYTHON_PATH, "ailibs_data", "testing", "images", "faces_1.jpg")
    LOG_TIME = True
    data_path = os.path.join(PYTHON_PATH, "ailibs_data")
    shape_predictor_path = os.path.join(data_path, "extractor", "dlib", "shape_predictor_68_face_landmarks.dat")
    face_recognition_path = os.path.join(data_path, "extractor", "dlib", "dlib_face_recognition_resnet_model_v1.dat")
    feature_path = os.path.join(data_path, "classifier", "resnet", "features.pickle")
    # classname_path = "/opt/webapps/Phuc_FCI20200819/facecheckin/streaming/storage/dbclassifiers/0/classname.pickle"
    # model_path = "/opt/webapps/Phuc_FCI20200819/facecheckin/streaming/storage/dbclassifiers/0/model.h5"
    image = cv2.imread(path)

    print(path, image.shape)

    detector = FaceDetector(log=False)
    extractor = FaceExtractor(shape_predictor=shape_predictor_path, face_recognition=face_recognition_path, log=True)
    classifier = FaceClassifier(feature=feature_path, log=True)

    dets = detector.detect(image)
    # print(dets, type(dets))
    features_list = []
    for d in dets:
        [left, top, right, bottom] = FaceDetector.get_position(d)
        print([left, top, right, bottom])
        f = extractor.extract(image, d)
        features_list.append(f)

    results = classifier.classify_list(features_list)
    print('__classify_list__', results)