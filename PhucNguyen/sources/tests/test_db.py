from time import time
import cv2
import os
import json
import django
from __init__ import PYTHON_PATH
os.environ['DJANGO_SETTINGS_MODULE'] = 'checkin.settings'
django.setup()

from utils.ConfigurationStatus import update_db as DB_UPDATED_CHECKIN
from checkin.facecheckin.models import Employee, FaceImage, CheckInTime, Configuration, PretrainedImage

# image = cv2.imread("/opt/webapps/FCI20200826/ai-research-topic/projects/FCI/storage/dbfaces/NiTran/0000028027.jpg")

# user_id = "NiTran"
# user = Employee(id=user_id,
#                             name=user_id,
#                             dob="19912008",
#                             level=1,
#                             description="description")
# user.save()

# start_time = int(time())
# checkin = {"employee_id": user_id,
# "start_time":start_time,
# "end_time":int(time())}

# configs = CheckInTime.objects.all()
# for a in configs:
#     print("__1111CheckInTime__", a.employee_id, a.start_time, a.end_time)

# print("Creating ???")
# DB_UPDATED_CHECKIN(checkin, image)
# # sleep(3)

# configs = CheckInTime.objects.all()
# for a in configs:
#     print("__222CheckInTime__", a.employee_id, a.start_time, a.end_time)


# print("Updating ???")
# checkin = {"employee_id": user_id,
# "start_time":start_time,
# "end_time":int(time())+5}
# DB_UPDATED_CHECKIN(checkin, image)

# configs = CheckInTime.objects.all()
# for a in configs:
#     print("__3333CheckInTime__", a.employee_id, a.start_time, a.end_time)


# print("Creating ???")
# checkin = {"employee_id": user_id,
# "start_time":int(time())+10,
# "end_time":int(time())+10}
# DB_UPDATED_CHECKIN(checkin, image)

# configs = CheckInTime.objects.all()
# for a in configs:
#     print("__4444CheckInTime__", a.employee_id, a.start_time, a.end_time)
# user_id = "PhucNguyen"
# data = list(PretrainedImage.objects.filter(
#             employee__id=user_id).values_list('id', flat=True))
# print(data)

import subprocess
PYTHONPATH = "/home/jetson02/Documents/phuc/facereg_cnn/FCI_Database_P/sources"
command = "nohup bash {}/trainning/trainning.sh &".format(PYTHONPATH)
subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
print("__________done")