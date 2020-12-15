from django.shortcuts import render, render_to_response
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import View
from django.template import RequestContext
from django.conf import settings

import json
import os

response_dict = {
    'settings': ''
}
PYTHONPATH = getattr(settings, 'PYTHONPATH')
CONFIG_PATH = os.path.join(PYTHONPATH, "checkin", "facecheckin", "configs", "config.txt")

FCI_HOST = getattr(settings, 'FCI_HOST')
FCI_STREAMING_PORT = getattr(settings, 'FCI_STREAMING_PORT')
FCI_API_PORT = getattr(settings, 'FCI_API_PORT')


# Update congiguration file
data = {}
data['HostName'] = FCI_HOST
data['PortAPI'] = FCI_API_PORT
data['PortCamera'] = FCI_STREAMING_PORT
data['NumberEmployee'] = 10
with open(CONFIG_PATH, 'w') as outfile:
    json.dump(data, outfile)


def update_config():
    with open(CONFIG_PATH) as json_file:
        data = json.load(json_file)
        domain = "http://" + data["HostName"] + ":" + data["PortAPI"]
        domainCamera = "http://" + data["HostName"] + ":" + data["PortCamera"]
        endPoint = settings.API_ENDPOINT
        res = {}
        res['SHOW_TIMESHEET'] = domain + endPoint["SHOW_TIMESHEET"]
        res['REGISTER_USER'] = domain + endPoint['REGISTER_USER']
        res['SHOW_IMAGE'] = domain + endPoint['SHOW_IMAGE']
        res['GET_ATTRIBUTE'] = domain + endPoint['GET_ATTRIBUTE']
        res['DOWNLOAD_TIMESHEET'] = domain + endPoint['DOWNLOAD_TIMESHEET']
        res["GET_USERS"] = domain + endPoint["GET_USERS"]
        res["VIDEO_STREAM"] = domainCamera + endPoint["VIDEO_STREAM"]
        res["NUMBER_EMPLOYEE"] = data["NumberEmployee"]
        res["CAMERA_CONFIG_URL"] = domain + endPoint["CAMERA_CONFIG_URL"]
        res["GET_USER_IMAGE"] = domain + endPoint["GET_USER_IMAGE"]
        res["SHOW_USER_IMAGE"] = domain + endPoint["SHOW_USER_IMAGE"]
        res["DELETE_USER_IMAGE"] = domain + endPoint["DELETE_USER_IMAGE"]
        res["CAMERA_CONFIG_ATTRIBUTES"] = domain + endPoint["CAMERA_CONFIG_ATTRIBUTES"]
        res["GET_UPDATE_USER_URL"] = domain + endPoint["GET_UPDATE_USER_URL"]

        response_dict['settings'] = res

# Create your views here.
def index(request):
    update_config()
    return render_to_response('pages/home.html', response_dict)

def user(request):
    update_config()
    return render_to_response('pages/user.html', response_dict)

def employees(request):
    update_config()
    return render_to_response('pages/employees.html', response_dict)

def config(request):
    update_config()
    with open(CONFIG_PATH) as json_file:
        data = json.load(json_file)
        domain = {
            'hostname' : data["HostName"],
            'portApi': data["PortAPI"],
            'portCamera' : data["PortCamera"],
            'nEmployee' : data["NumberEmployee"]
        }
        response_dict['settings']['domain'] = domain
        return render(request, 'pages/config.html', response_dict)

class  ConfigUpdate(View):
    def post(self, request):
        response_data = {
            'status' : 1
        }
        hostname = request.POST.get('domain[hostname]')
        portAPI = request.POST.get('domain[portApi]')
        portCamera = request.POST.get('domain[portCamera]')
        numberEmployee = request.POST.get('domain[numberEmployee]')
        data = {}
        data['HostName'] = hostname
        data['PortAPI'] = portAPI
        data['PortCamera'] = portCamera
        data['NumberEmployee'] = numberEmployee
        with open(CONFIG_PATH, 'w') as outfile:
            json.dump(data, outfile)
        return JsonResponse(response_data)