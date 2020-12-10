import os
import json
import django
from __init__ import PYTHON_PATH
os.environ['DJANGO_SETTINGS_MODULE'] = 'checkin.settings'
django.setup()

from checkin.facecheckin.models import Configuration, Employee


# load json configs
attribute_data_path = os.path.join(PYTHON_PATH, "tests", "camera_configs.json")
data = {}
with open(attribute_data_path) as file:
    data = json.load(file)
    file.close()
# record db
for k, v in data.items():
    config = Configuration(**v).save()

configs = Configuration.objects.all().values()
for config in configs:
    print("Configuration: ", config)


# creating Unknown user
user_id = "Unknown"
user = Employee(id=user_id,
                name=user_id,
                dob="19912008",
                level=1,
                description="Unknown")
user.save()