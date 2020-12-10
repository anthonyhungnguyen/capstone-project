import os
import json
import django
# from __init__ import PYTHON_PATH
os.environ['DJANGO_SETTINGS_MODULE'] = 'checkin.settings'

from utils.Status import TRAINING_STATUS, UPDATED_FACE_CLASSIFIER
from utils.ImageStorage import ImageStorage
from checkin.facecheckin.models import Employee, FaceImage, CheckInTime, Configuration, PretrainedImage
from utils.LogFCI import setup_logger

from django.conf import settings
STORAGE_LOCATION = getattr(settings, 'STORAGE_LOCATION')
MAXIMUM_FACE_PER_USER = getattr(settings, 'MAXIMUM_FACE_PER_USER')
PYTHONPATH = getattr(settings, 'PYTHONPATH')
LOG_STREAMING_PATH = getattr(settings, 'LOG_STREAMING_PATH')

IMAGESTORAGE = ImageStorage(STORAGE_LOCATION)

STREAMING_NOT_DEFINED = "none"
CHECKIN_DURATION = 30 #seconds
TRAINING_STATUS_DEFAULT = "none"

class CAMERA_CONFIG:
    LOGGER = setup_logger('streaming', LOG_STREAMING_PATH)
    CAMERA_URL = 0
    USER_ID = STREAMING_NOT_DEFINED
    TRAINING_STATUS = TRAINING_STATUS_DEFAULT
    FR_TOTAL = MAXIMUM_FACE_PER_USER
        
    def update():
        CAMERA_CONFIG.CAMERA_URL = Configuration.objects.get(key="camera_url").value
        if CAMERA_CONFIG.CAMERA_URL == "0":
            CAMERA_CONFIG.CAMERA_URL = 0
        CAMERA_CONFIG.USER_ID = Configuration.objects.get(key="streaming_user_id").value
        CAMERA_CONFIG.TRAINING_STATUS = Configuration.objects.get(key="training_status").value

    def deregister():
        CAMERA_CONFIG.LOGGER.info("Stop registering for {}.".format(CAMERA_CONFIG.USER_ID))
        Configuration.objects.filter(key="streaming_user_id").update(value=STREAMING_NOT_DEFINED)
        CAMERA_CONFIG.USER_ID = STREAMING_NOT_DEFINED

def update_db(info, face_imag):
    try:
        image = FaceImage()
        image.save()
        IMAGESTORAGE.write(face_imag, getattr(image, "id"))

        info['image_id'] = getattr(image, "id")
        records = CheckInTime.objects.filter(employee__id=info['employee_id'], end_time__gte=info['end_time']-CHECKIN_DURATION).update(end_time=info['end_time'])
        if not records:
            emp =  Employee.objects.get(id=info['employee_id'])
            if not emp:
                raise Exception("Invalid Employee {}".format(info['employee_id']))

            checkin = CheckInTime(employee_id=info['employee_id'],
                                image_id=info['image_id'],
                                start_time=info['start_time'],
                                end_time=info['end_time'])
            checkin.save()
            CAMERA_CONFIG.LOGGER.info("Creating CheckInTime for {} at {}".format(info['employee_id'], info['start_time']))
        # else: 
        #     print(">>>Updating CheckInTime")
    except Exception as e:
        CAMERA_CONFIG.LOGGER.error(e)
