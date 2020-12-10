import os
import cv2
import shutil
import django

from __init__ import PYTHON_PATH
from ailibs.utils import utils as UTILS
os.environ['DJANGO_SETTINGS_MODULE'] = 'checkin.settings'
django.setup()
from checkin.facecheckin.models import Employee, PretrainedImage

IN_dbfaces_path = "/home/jetson02/Documents/phuc/facereg_cnn/FCI_Database_P/dbfaces"
OUT_dbfaces_path = "/home/jetson02/Documents/phuc/facereg_cnn/FCI_Database_P/storage/dbfaces"

IN_user_list = os.listdir(IN_dbfaces_path)
for IN_user in IN_user_list:
    # create usser in db

    try:
        user = Employee(id=IN_user,
                            name=IN_user,
                            dob="19950102",
                            level=0,
                            description="description")
        user.save()
        print("Creating user = {}".format(IN_user))
    except Exception as e:
        print("Employee", e)
    
    IN_user_path = os.path.join(IN_dbfaces_path, IN_user)
    IN_image_list = os.listdir(IN_user_path)

    OUT_user_path = os.path.join(OUT_dbfaces_path, IN_user)
    if not os.path.isdir(OUT_user_path):
        os.mkdir(OUT_user_path)
    else: 
        pass
    for i, image in enumerate(IN_image_list):
        if i == 300: 
            break
        # create image in db
        pretrain = PretrainedImage(employee_id=IN_user)
        pretrain.save()

        IN_image_path = os.path.join(IN_user_path, image)
        OUT_image_path = os.path.join(OUT_user_path, str(pretrain.id)+'.jpg')
        shutil.copy(IN_image_path,OUT_image_path)
        # cv2.imwrite(image_name, face)
        # print("Saved {}: {} to {} for {}".format(i, image, pretrain.id, IN_user))
        # copy image to dbfaces_path
    print(">>> User {}: {} face imges".format(IN_user, len(IN_image_list)))