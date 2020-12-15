# import json
# import cv2
# import numpy
# import os
# import base64
# from PIL import Image
# import ast
# import yaml
# import traceback

# Django library
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files import File
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render


# Helper modules
# from ps.httphelper import Matrix
from checkin.facecheckin.httprrrors import HttpErrors
# from ps.httphelper import ResponseModel
# from ps.httphelper import HTTPHelper
from checkin import views
from checkin.facecheckin import settings
# from cvlib.utils import Log

# CVCORE_SERVICE = ServiceProvider()
# LOGGER = Log.log

@csrf_exempt
def index(request):
    """
    Render index page.

    Args:
        request (json): request.
    Returns:
        response (json): response.
    """

    hostIP = request.get_host()
    templateData = {
        'hostIP': hostIP
    }
    try:
        response = render(request, 'index.html', templateData)
    except Exception as e:
        raise e
        # LOGGER.error("Exception found! %s" %e)
    return response

@csrf_exempt
def settings(request):
    """
    Render index page.

    Args:
        request (json): request.
    Returns:
        response (json): response.
    """

    hostIP = request.get_host()
    templateData = {
        'hostIP': hostIP
    }
    try:
        response = render(request, 'settings.html', templateData)
    except Exception as e:
        raise e
        # LOGGER.error("Exception found! %s" %e)
    return response

@csrf_exempt
def frameList(request):
    """
    Render index page.

    Args:
        request (json): request.
    Returns:
        response (json): response.
    """

    hostIP = request.get_host()
    templateData = {
        'hostIP': hostIP
    }
    try:
        response = render(request, 'frameList.html', templateData)
    except Exception as e:
        raise e
        # LOGGER.error("Exception found! %s" %e)
    return response

# @csrf_exempt
# def showFrameList(request):
#     """
#     Show frame list.

#     Args:
#         request (json): request.
#     Returns:
#         response (json): response.
#     """

#     # Parse and get data from request
#     if request.method == 'POST':
#         try:
#             requestBody = views.handle_request_content(request)

#             #object_id = int(requestBody['object_id'])
#             time_range = views.convertToList(requestBody['time_range'])
#             rawFrameSize = requestBody.get('frame_size', None)
#             frame_size = None
#             if rawFrameSize is not None:
#                 frame_size = numpy.array(numpy.mat(rawFrameSize)).reshape(-1)
#             show_rectangle = bool(requestBody.get("show_rectangle", "") in views.ALLOWED_BOOLEAN_VALUE)
#             crop_result = bool(requestBody.get("crop_result", "") in views.ALLOWED_BOOLEAN_VALUE)
#             confidence = float(requestBody.get('confidence', THRESHOLD.OBJECT_MAX_CONFIDENCE) or 1.0)
#             face_total = int(requestBody.get('face_total', 100) or 100)
#             images = views.handle_uploaded_files(request)
#         except Exception as ex:
#             return HttpErrors.serverErrorHandler(request=request, exception=ex)
#     else:
#         return HttpErrors.METHOD_NOT_ALLOWED_405


#     data = CVCORE_SERVICE.objectSearch(views.FACE_SEARCH_OBJECT_TYPE,
#         time_range, confidence, face_total, images[0])

#     # hostIP = '172.18.14.15:8000'
#     hostIP = request.get_host()
#     showedImage = []
#     for item in data:
#         frameList = CVCORE_SERVICE.showImageList(hostIP,
#             item.get('object_id'), time_range,
#             item.get('frame_size'), show_rectangle,
#             crop_result)
#         showedImage += frameList

#     templateData = {
#         'imgList': showedImage,
#         'hostIP': hostIP
#     }
#     return render(request, 'index.html', templateData)
