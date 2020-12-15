from utils.LogFCI import setup_logger
from utils.ConfigurationStatus import TRAINING_STATUS
from utils.ImageStorage import ImageStorage
from checkin.facecheckin.models import Employee, FaceImage, CheckInTime, Configuration, PretrainedImage
from checkin.facecheckin.httperrors import HttpErrors
from utils.mail_alert.MailAlert import MailAlert
import os
import json
import time
import pytz
import cv2
import pandas
from PIL import Image
from datetime import datetime
import subprocess
import uuid

import mimetypes
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
BASE_DIR = getattr(settings, 'BASE_DIR')
PYTHONPATH = getattr(settings, 'PYTHONPATH')
STORAGE_ROOT = getattr(settings, 'STORAGE_ROOT')
STORAGE_LOCATION = getattr(settings, 'STORAGE_LOCATION')
RECENT_TIME_DURATION = getattr(settings, 'RECENT_TIME_DURATION')
TIMESHEET_PATH = getattr(settings, 'TIMESHEET_PATH')
LOCAL_TIMEZONE = getattr(settings, 'LOCAL_TIMEZONE')
MAXIMUM_LENGTH_IMAGE = getattr(settings, 'MAXIMUM_LENGTH_IMAGE')
FCI_STREAMING_PORT = getattr(settings, 'FCI_STREAMING_PORT')
LOG_API_PATH = getattr(settings, 'LOG_API_PATH')

LOGGER = setup_logger('api', LOG_API_PATH)
utils_path = os.path.join(PYTHONPATH, "utils")
mail_receiver_path = os.path.join(
    utils_path, "mail_alert", "receiver_address.txt")
alert_image_path = os.path.join(utils_path, "mail_alert", "images")

MAIL_ALERT = MailAlert(mail_receiver=mail_receiver_path,
                        images=alert_image_path)

IMAGESTORAGE = ImageStorage(STORAGE_LOCATION)

EMPTY_STRING = ""
NOT_DEFINED_VALUE = -1
DELETED_VALUE = -2
UNKNOWN = "Unknown"
STREAMING_NOT_DEFINED = "none"


class STATUS:
    NOT_DEFINED = -1
    FAILED = 0
    SUCCESS = 1


class STREAMING_STATUS:
    NOT_DEFINED = -1
    START = 0
    STOP = 1


class LEVEL:
    NOT_DEFINED = -1
    EMPLOYEE = 0
    LEADER = 1
    MANAGER = 2


def convert_string_to_list(shape_list):
    """
    Convert tring to list

    Args:
        shape_list(str): list as tring

    Returns:
        shape_list(str): list as list type

    """
    if isinstance(shape_list, str):
        if shape_list not in ['[]', '', ""]:
            shape_list = shape_list.replace("[", "")
            shape_list = []
    shape_list = [x for x in shape_list]
    return shape_list


def handle_request_content(request):
    """
    Handle request content.

    Args:
        request (json): request as json string.
    Returns:
        content (dictionary): request data as dictionary.
    """
    if hasattr(request.META, 'CONTENT_TYPE') and request.META['CONTENT_TYPE'] == 'application/json':
        stringData = request.body.decode('utf-8')
        return json.loads(stringData)
    else:
        return request.POST


def download_file(url):
    """
    Download file.

    Args:
        file_path (str): file path.
    Returns:
        response (HttpResponse): response

    """
    ext = url[4:]
    file_path = os.path.join(BASE_DIR, url)
    csv_file = open(file_path, 'r')
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(csv_file, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % ext

    return response


def get_timesheet(id_list, start_time, end_time):

    data = []

    try:
        id_list = convert_string_to_list(id_list)
        if end_time == NOT_DEFINED_VALUE or start_time == NOT_DEFINED_VALUE:
            end_time = int(time.time())
            start_time = int(end_time - RECENT_TIME_DURATION)

        if end_time < start_time:
            end_time = start_time

        user_list = Employee.objects.all().exclude(id=UNKNOWN)
        id_list = [str(i) for i in id_list]
        if id_list:
            user_list = user_list.filter(id__in=id_list)
        user_list = list(user_list.values())

        for user in user_list:
            record_list = list(CheckInTime.objects.filter(employee_id=user["id"],
                                                          start_time__gte=start_time,
                                                          start_time__lte=end_time,
                                                          end_time__gte=start_time,
                                                          end_time__lte=end_time).values())

            for record in record_list:
                record["user_id"] = user["id"]
                record["name"] = user["name"]
                start_dt = datetime.fromtimestamp(
                    record["start_time"]).astimezone(pytz.timezone(LOCAL_TIMEZONE))
                end_dt = datetime.fromtimestamp(record["end_time"]).astimezone(
                    pytz.timezone(LOCAL_TIMEZONE))
                record["start_time_datetime"] = str(start_dt)
                record["end_time_datetime"] = str(end_dt)
                del record["employee_id"]
                del record["id"]
                record['image_id'] = str(record['image_id'])
                data.append(record)
        data = sorted(data, key=lambda i: i['end_time'], reverse=False)
        return data
    except Exception as e:
        raise e


@csrf_exempt
def download_timesheet(request):
    """
    Download csv file.

    Args:
        file_path (str): file path.
    Returns:
        response (HttpResponse): response

    """
    if request.method == 'POST':
        try:
            requestBody = handle_request_content(request)
            start_time = int(requestBody.get("start_time", NOT_DEFINED_VALUE))
            end_time = int(requestBody.get("end_time", NOT_DEFINED_VALUE))
        except Exception as e:
            LOGGER.error("%s", str(e))
            return HttpErrors.serverErrorHandler(request=request, exception=e)
    else:
        return HttpErrors.METHOD_NOT_ALLOWED_405

    id_list = []
    data = get_timesheet(id_list, start_time, end_time)

    # Save timesheet as csv file
    dataframe = pandas.DataFrame(data)
    name = str(int(time.time())) + ".csv"
    file_path = os.path.join(TIMESHEET_PATH, name)
    save_path = os.path.join(BASE_DIR, file_path)
    dataframe.to_csv(save_path, encoding='utf-8', index=False)

    # Download timesheet file
    response = download_file(file_path)

    return response


@csrf_exempt
def get_attributes(request):
    """

    Args:
        request:

    Returns:

    """
    response = {}
    response["message"] = EMPTY_STRING
    response["status"] = STATUS.NOT_DEFINED
    response["data_list"] = {}
    # Parse and get data from request
    if request.method == 'GET':
        attribute_data_path = os.path.join(
            BASE_DIR, "checkin", "facecheckin", "configs", "attribute_data")
        data = {}
        with open(attribute_data_path) as file:
            data = json.load(file)
            file.close()
    else:
        return HttpErrors.METHOD_NOT_ALLOWED_405

    # Camera configuration
    configs = Configuration.objects.values()
    camera_configs = {}
    for item in configs:
        camera_configs[str(item["key"])] = str(item["value"])

    response["data_list"] = data
    response["data_list"]["camera_configs"] = camera_configs
    response["status"] = STATUS.SUCCESS
    LOGGER.info("get_attributes()", data)
    return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
def get_camera_config(request):
    """

    Args:
        request:

    Returns:

    """
    response = {}
    response["message"] = EMPTY_STRING
    response["status"] = STATUS.NOT_DEFINED

    try:
        # Camera configuration
        configs = Configuration.objects.values()
        camera_configs = []
        for item in configs:
            field = {}

            field['name'] = item["key"]
            field['value'] = item["value"]
            field['default'] = item["default_value"]
            if item["edit"].lower() == "true":
                field['edit'] = True
            else:
                field['edit'] = False
            camera_configs.append(field)

        camera_configs = sorted(camera_configs, key=lambda i: i['name'])

        response["camera_configs"] = camera_configs
        response["status"] = STATUS.SUCCESS
    except Exception as e:
        LOGGER.error("%s", str(e))
        response["status"] = STATUS.FAILED
        response["message"] = str(e)
    finally:
        httpResponse = HttpResponse(
            json.dumps(response), content_type='application/json')
        return httpResponse


@csrf_exempt
def set_camera_config(request):
    """
    Update camera configuration.

    Args:
        file_path (str): file path.
    Returns:
        response (HttpResponse): response

    """
    response = {}
    response["message"] = EMPTY_STRING
    response["status"] = STATUS.NOT_DEFINED
    try:
        if request.method == 'POST':
            try:
                requestBody = handle_request_content(request)
                camera_url = str(requestBody.get("camera_url", EMPTY_STRING))
                camera_width = str(requestBody.get(
                    "camera_width", EMPTY_STRING))
                camera_height = str(requestBody.get(
                    "camera_height", EMPTY_STRING))
                detector_mode = str(requestBody.get(
                    "detector_mode", EMPTY_STRING))
                face_range_ratio = str(requestBody.get(
                    "face_range_ratio", EMPTY_STRING))
                detector_skip_frame = str(requestBody.get(
                    "detector_skip_frame", EMPTY_STRING))
                normalizer_mode = str(requestBody.get(
                    "normalizer_mode", EMPTY_STRING))
                tracker_mode = str(requestBody.get(
                    "tracker_mode", EMPTY_STRING))
                extractor_mode = str(requestBody.get(
                    "extractor_mode", EMPTY_STRING))
                classifier_mode = str(requestBody.get(
                    "classifier_mode", EMPTY_STRING))
                classifier_threshold = requestBody.get(
                    "classifier_threshold", EMPTY_STRING)
                classifier_max_name_list = str(requestBody.get(
                    "classifier_max_name_list", EMPTY_STRING))
                processing_time = requestBody.get(
                    "processing_time", EMPTY_STRING)
                skip_frame_count = str(requestBody.get(
                    "skip_frame_count", EMPTY_STRING))
                streaming_user_id = requestBody.get(
                    "streaming_user_id", EMPTY_STRING)
                streaming_duration = str(requestBody.get(
                    "streaming_duration", EMPTY_STRING))
                training_status = str(requestBody.get(
                    "training_status", EMPTY_STRING))
                update_face_classifier = str(requestBody.get(
                    "update_face_classifier", EMPTY_STRING))
                checkin_mode = str(requestBody.get(
                    "checkin_mode", EMPTY_STRING))

            except Exception as e:
                LOGGER.error("Exception %s", str(e))
                return HttpErrors.serverErrorHandler(request=request, exception=e)
        else:
            return HttpErrors.METHOD_NOT_ALLOWED_405

        configs = {}
        configs['camera_url'] = camera_url
        configs['camera_width'] = camera_width
        configs['camera_height'] = camera_height
        configs['detector_mode'] = detector_mode
        configs['face_range_ratio'] = face_range_ratio
        configs['detector_skip_frame'] = detector_skip_frame
        configs['normalizer_mode'] = normalizer_mode
        configs['tracker_mode'] = tracker_mode
        configs['extractor_mode'] = extractor_mode
        configs['classifier_mode'] = classifier_mode
        configs['classifier_threshold'] = classifier_threshold
        configs['classifier_max_name_list'] = classifier_max_name_list
        configs['processing_time'] = processing_time
        configs['skip_frame_count'] = skip_frame_count
        configs['streaming_user_id'] = streaming_user_id
        configs['streaming_duration'] = streaming_duration
        configs['training_status'] = training_status
        configs['update_face_classifier'] = update_face_classifier
        configs['checkin_mode'] = checkin_mode

        for key, value in configs.items():
            if value != EMPTY_STRING:
                LOGGER.info("Updating {} into {}".format(key, value))
                Configuration.objects.filter(key=key).update(value=value)

        if configs['training_status'] == TRAINING_STATUS.START:
            command = "nohup bash {}/trainning/trainning.sh &".format(PYTHONPATH)
            subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            # command = "fuser -n tcp -k {}".format(FCI_STREAMING_PORT)
            # subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

        response["status"] = STATUS.SUCCESS
    except Exception as e:
        response["message"] = str(e)
        response["status"] = STATUS.FAILED

    finally:
        httpResponse = HttpResponse(
            json.dumps(response), content_type='application/json')
        return httpResponse


@csrf_exempt
def show_image(request):
    """

    Args:
        request:

    Returns:

    """
    # Parse and get data from request
    if request.method == 'GET':
        requestBody = request.GET
        image_id = str(requestBody['image_id'])
    else:
        return HttpErrors.METHOD_NOT_ALLOWED_405
    image = None
    image = IMAGESTORAGE.read(image_id)
    if image is None:
        not_found_image_path = os.path.join(
            BASE_DIR, "ailibs_data", "testing", "images", "notfound.jpg")
        image = cv2.imread(not_found_image_path)

    # Convert brg to rgb
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Convert numpy array to Image object
    image = Image.fromarray(image)
    print("IMAGE: ", image)
    response = HttpResponse(content_type='image/jpeg')
    image.save(response, 'JPEG')
    return response


@csrf_exempt
def register_user(request):
    """

    Args:
        request:

    Returns:

    """
    response = {}
    response["message"] = EMPTY_STRING
    response["status"] = STATUS.NOT_DEFINED
    # Parse and get data from request
    try:
        if request.method == 'POST':
            try:
                requestBody = handle_request_content(request)
                user_id = requestBody.get("user_id", EMPTY_STRING)
                name = requestBody.get("name", EMPTY_STRING)
                dob = requestBody.get("dob", EMPTY_STRING)
                level = int(requestBody.get("level", STATUS.NOT_DEFINED))
                description = requestBody.get("description", EMPTY_STRING)
                streaming_status = int(requestBody.get(
                    "streaming_status", STREAMING_STATUS.NOT_DEFINED))
                delete_status = int(requestBody.get(
                    "delete_status", STATUS.NOT_DEFINED))
            except Exception as e:
                LOGGER.error("%s", str(e))
                return HttpErrors.serverErrorHandler(request=request, exception=e)
        else:
            return HttpErrors.METHOD_NOT_ALLOWED_405

        LOGGER.info(" Register/Update user_id = %s, name = %s, dob = %s, level = %s, description = %s, streaming_status = %s, delete_status = %s",
                    str(user_id), str(name), str(dob), str(level), str(description), str(streaming_status), str(delete_status))
        # Get new system mode
        newSystemMode = {}
        if user_id == EMPTY_STRING:
            message = "user_id = [{}] is invalid!".format(user_id)
            LOGGER.error(message)
            raise Exception(message)
        if name == EMPTY_STRING:
            message = "name = [{}] is invalid!".format(name)
            LOGGER.error(message)
            raise Exception(message)
        if dob == EMPTY_STRING:
            message = "dob = [{}] is invalid!".format(dob)
            LOGGER.error(message)
            raise Exception(message)
        if level == STATUS.NOT_DEFINED:
            level = LEVEL.EMPLOYEE

        user = None
        user_id = str(user_id.replace("\"", ""))
        name = str(name.replace("\"", ""))
        dob = str(dob.replace("\"", ""))
        description = str(description.replace("\"", ""))
        try:
            user = Employee.objects.get(id=user_id)
            if delete_status == DELETED_VALUE:
                LOGGER.info("Delete user_id = %s", str(user_id))
                user.delete()
                response["user_id"] = user_id
                response["message"] = "The user_id <{}> is deleted !".format(
                    user_id)
                response["status"] = STATUS.SUCCESS
                return

            # Update fields
            LOGGER.info("Update user_id = %s", str(user_id))
            user.name = name
            user.dob = dob
            user.level = level
            user.description = description
            user.save()
        except Exception as e:
            if delete_status == DELETED_VALUE:
                response["message"] = "The user_id <{}> does not exist in database !".format(
                    user_id)
                response["status"] = STATUS.SUCCESS
                return

            LOGGER.info("Create new user_id = %s", str(user_id))
            user = Employee(id=user_id,
                            name=name,
                            dob=dob,
                            level=level,
                            description=description)
            user.save()
        # TODO #nartin handle
        # streaming_status
        # generated_frames = os.path.join(BASE_DIR, "register", "start_generating_frames.py")
        if streaming_status == STREAMING_STATUS.START:
            # start record video
            LOGGER.info("Start streaming video for user_id = %s", str(user_id))
            config = Configuration.objects.filter(key="streaming_user_id")[0]
            Configuration.objects.filter(
                key="streaming_user_id").update(value=user_id)
            # pass
            # subprocess.call(["python", os.path.join(BASE_DIR, "register", "start_generating_frames.py"),
            #                 "--user_id", user_id,
            #                 "--camera_url", CAMERA_URL,
            #                 "--db_path", DBIMAGES_LOCATION])

        elif streaming_status == STREAMING_STATUS.STOP:
            # stop record video
            LOGGER.info("Stop streaming video for user_id = %s", str(user_id))
            Configuration.objects.filter(key="streaming_user_id").update(
                value=STREAMING_NOT_DEFINED)
            # pass
            # subprocess.call(["python", os.path.join(BASE_DIR, "register", "stop_generating_frames.py"),
            #                 "--process_name", os.path.join(BASE_DIR, "register", "start_generating_frames.py"),
            #                 "--user_id", user_id])

        response["status"] = STATUS.SUCCESS
        response["user_id"] = user.id

    except Exception as e:
        LOGGER.error("%s", str(e))
        response["message"] = str(e)
        response["status"] = STATUS.FAILED

    finally:
        LOGGER.info("register_user()", response)
        httpResponse = HttpResponse(
            json.dumps(response), content_type='application/json')
        return httpResponse


@csrf_exempt
def show_timesheet(request):
    """

    Args:
        request:

    Returns:

    """

    response = {}
    response["message"] = EMPTY_STRING
    response["status"] = STATUS.NOT_DEFINED
    response["data_list"] = []
    # Parse and get data from request
    try:
        if request.method == 'POST':
            try:
                requestBody = handle_request_content(request)
                id_list = []
                start_time = int(requestBody.get(
                    "start_time", NOT_DEFINED_VALUE))
                end_time = int(requestBody.get("end_time", NOT_DEFINED_VALUE))
            except Exception as e:
                LOGGER.error("%s", str(e))
                raise e
        else:
            return HttpErrors.METHOD_NOT_ALLOWED_405

        # MAIL_ALERT
        if MAIL_ALERT.check_alert():
            print("MAIL_ALERT", MAIL_ALERT.check_alert())
            MAIL_ALERT.send_alert()

        id_list = []
        data = get_timesheet(id_list, start_time, end_time+1)
        response["status"] = STATUS.SUCCESS
        response["data_list"] = data

    except Exception as e:
        response["message"] = str(e)
        response["status"] = STATUS.FAILED

    finally:
        httpResponse = HttpResponse(
            json.dumps(response), content_type='application/json')
        return httpResponse


@csrf_exempt
def get_users_information(request):
    """

    Args:
        request:

    Returns:

    """
    response = {}
    response["message"] = EMPTY_STRING
    response["status"] = STATUS.NOT_DEFINED
    response["data_list"] = []
    # Parse and get data from request
    try:
        if request.method == 'POST':
            try:
                requestBody = handle_request_content(request)
                user_id = requestBody.get("user_id", "")
            except Exception as e:
                LOGGER.error("%s", str(e))
                return HttpErrors.serverErrorHandler(request=request, exception=e)
        else:
            return HttpErrors.METHOD_NOT_ALLOWED_405

        # Load database
        user_list = Employee.objects.all()
        if user_id != EMPTY_STRING:
            user_list = user_list.filter(id=user_id)
        user_list = list(user_list.values())
        user_list = [user for user in user_list if user['id'] != 'Unknown']
        for user in user_list:
            user["image_id"] = str(user["image_id"])
            pretrainedimage_id = PretrainedImage.objects.filter(employee_id=user["id"]).last()
            user["pretrainedimage_id"] =  ''
            if pretrainedimage_id is not None:
                user["pretrainedimage_id"] = str(pretrainedimage_id.id)
                # TODO
            user["activate"] = 1

        for i in range(len(user_list)):
            if not user_list[i]["image_id"]:
                try:
                    checkin_record = CheckInTime.objects.filter(
                        employee_id=user_list[i]["id"]).order_by("id")
                    if checkin_record:
                        # Employee.objects.filter(id=user_list[i]["id"]).update(
                        #     image_id=checkin_record[0].image_id, activate=1)
                        user_list[i]["image_id"] = str(checkin_record.image_id)
                        
                        user_list[i]["activate"] = 1
                        LOGGER.info("Update image_id of user_id =%s to %s", str(
                            user_list[i]["id"]), str(checkin_record.image_id))
                    else:
                        user_list[i]["image_id"] = ""
                except Exception as e:
                    LOGGER.info("%s", str(e))
                    user_list[i]["image_id"] = ""
            user_list[i]["user_id"] = user_list[i]["id"]
            del user_list[i]["id"]

        response["data_list"] = user_list
        response["status"] = STATUS.SUCCESS

    except Exception as e:
        response["message"] = str(e)
        response["status"] = STATUS.FAILED

    finally:
        httpResponse = HttpResponse(
            json.dumps(response), content_type='application/json')
        return httpResponse


@csrf_exempt
def get_user_images(request):
    """

    Args:
        request:

    Returns:

    """

    response = {}
    response["message"] = EMPTY_STRING
    response["status"] = STATUS.NOT_DEFINED
    response["data_list"] = []
    # Parse and get data from request
    try:
        if request.method == 'POST':
            try:
                requestBody = handle_request_content(request)
                user_id = str(requestBody.get("user_id", EMPTY_STRING))
            except Exception as e:
                LOGGER.error("%s", str(e))
                raise e
        else:
            return HttpErrors.METHOD_NOT_ALLOWED_405

        if user_id == EMPTY_STRING:
            message = "user_id = [{}] is invalid!".format(user_id)
            LOGGER.error(message)
            raise Exception(message)

        # Get user info

        user = Employee.objects.filter(id=user_id)
        if not user:
            message = "user_id = [{}] is not existed in database!".format(
                user_id)
            LOGGER.error(message)
            raise Exception(message)

        user = user[0]
        response['user_id'] = user.id
        response['name'] = user.name
        response['dob'] = user.dob
        response['level'] = user.level
        response['activate'] = user.activate
        response['image_id'] = str(user.image_id)
        if user.image_id is None:
            response['image_id'] = ""
        response['description'] = user.description

        LOGGER.info("user_id = %s", str(user_id))
        data = list(PretrainedImage.objects.filter(
            employee__id=user_id).values_list('id', flat=True))

        # data = data[:50] #TODO
        data = [str(dat) for dat in data]
        response['pretrainedimage_id'] = ""
        if len(data) > 0:
            response['pretrainedimage_id'] = str(data[0])
        response["status"] = STATUS.SUCCESS
        response["data_list"] = data

    except Exception as e:
        response["message"] = str(e)
        response["status"] = STATUS.FAILED

    finally:
        httpResponse = HttpResponse(
            json.dumps(response), content_type='application/json')
        return httpResponse


@csrf_exempt
def show_user_image(request):
    """

    Args:
        request:

    Returns:

    """

    # Parse and get data from request
    if request.method == 'GET':
        requestBody = request.GET
        user_id = str(requestBody.get("user_id", EMPTY_STRING))
        user_image_id = str(requestBody.get("user_image_id", EMPTY_STRING))
    else:
        return HttpErrors.METHOD_NOT_ALLOWED_405

    if user_id == EMPTY_STRING:
        message = "user_id = [{}] is invalid!".format(user_id)
        LOGGER.error(message)

    if user_image_id == EMPTY_STRING:
        message = "user_image_id = [{}] is invalid!".format(user_image_id)
        LOGGER.error(message)

    image = None
    image_name = str(str(user_image_id)).zfill(MAXIMUM_LENGTH_IMAGE)+'.jpg'
    image_path = os.path.join(
        STORAGE_ROOT, "dbfaces", user_id, image_name)
    print("image_path", image_path)
    if os.path.exists(image_path):
        image = cv2.imread(image_path)
    if image is None:
        not_found_image_path = os.path.join(
            BASE_DIR, "ailibs_data", "testing", "images", "notfound.jpg")
        image = cv2.imread(not_found_image_path)

    # Convert brg to rgb
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Convert numpy array to Image object
    image = Image.fromarray(image)
    response = HttpResponse(content_type='image/jpeg')
    image.save(response, 'JPEG')
    return response


@csrf_exempt
def delete_user_image(request):
    """

    Args:
        request:

    Returns:

    """

    response = {}
    response["message"] = EMPTY_STRING
    response["status"] = STATUS.NOT_DEFINED
    # Parse and get data from request
    try:
        if request.method == 'POST':
            try:
                requestBody = handle_request_content(request)
                user_id = str(requestBody.get("user_id", EMPTY_STRING))
                user_image_id = str(requestBody.get(
                    "user_image_id", EMPTY_STRING))
            except Exception as e:
                LOGGER.error("%s", str(e))
                raise e
        else:
            return HttpErrors.METHOD_NOT_ALLOWED_405

        if user_id == EMPTY_STRING:
            message = "user_id = [{}] is invalid!".format(user_id)
            LOGGER.error(message)
            raise Exception(message)

        if user_id == EMPTY_STRING:
            message = "user_image_id = [{}] is invalid!".format(user_image_id)
            LOGGER.error(message)
            raise Exception(message)

        # Delete database object
        # id_img = uuid.UUID(user_image_id)
        # print("__________", user_image_id, type(user_image_id), id_img, type(id_img))
        LOGGER.info("Remove PretrainedImage object %s.", str(user_image_id))
        obj = PretrainedImage.objects.filter(
            employee__id=user_id, id=uuid.UUID(user_image_id))
        if obj:
            obj.delete()
            # pass
        else:
            message = "user_id = [{}] and user_image_id = [{}] is not existed in database !".format(
                user_id, user_image_id)
            LOGGER.error(message)
            raise Exception(message)

        # Delete image file
        image_name = str(user_image_id).zfill(MAXIMUM_LENGTH_IMAGE)
        image_path = os.path.join(
            STORAGE_ROOT, "dbfaces", user_id, image_name + ".jpg")
        if os.path.exists(image_path):
            LOGGER.info("Remove file %s.", str(image_path))
            try:
                image = os.remove(image_path)
            except Exception as e:
                response["message"] += str(e)

        # # Delete face feature
        # feature_path = os.path.join(STORAGE_ROOT, "dbfeatures", user_id)
        # if not os.path.exists(feature_path):
        #     with open(feature_path) as file:
        #         feature_user = json.load(file)
        #     file.close()

        #     LOGGER.info("user_image_id ==== %s.", image_file_name)
        #     if image_file_name in feature_user:
        #         print("MAXIMUM_LENGT___________ %s", str(
        #             feature_user[image_file_name][:5]))
        #         del feature_user[image_file_name]

        #     with open(feature_path, 'w') as file:
        #         json.dump(feature_user, file, indent=2)
        #     file.close()

        response["status"] = STATUS.SUCCESS

    except Exception as e:
        response["message"] = str(e)
        response["status"] = STATUS.FAILED

    finally:
        LOGGER.info("user_id = %s, user_image_id = %s, response = %s",
                    str(user_id), str(user_image_id), str(response))
        httpResponse = HttpResponse(
            json.dumps(response), content_type='application/json')
        return httpResponse
