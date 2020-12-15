from django.conf.urls import url
from . import webviews
from . import views

urlpatterns = [
    # For webview
    url(r'^home', webviews.index),
    url(r'^user', webviews.user),
    url(r'^employees', webviews.employees),
    url(r'^config', webviews.config),
    url(r'^update', webviews.ConfigUpdate.as_view(), name='config_update'),

    # For BE
    url(r'^data/get_attributes', views.get_attributes),
    url(r'^data/get_camera_config', views.get_camera_config),
    url(r'^data/set_camera_config', views.set_camera_config),
    url(r'^data/register_user', views.register_user),
    url(r'^data/get_user_images', views.get_user_images),
    url(r'^data/show_user_image', views.show_user_image),
    url(r'^data/delete_user_image', views.delete_user_image),
    url(r'^data/register_user', views.register_user),
    url(r'^data/show_timesheet', views.show_timesheet),
    url(r'^data/show_image', views.show_image),
    url(r'^data/get_users_information', views.get_users_information),
    url(r'^data/download_timesheet', views.download_timesheet)
]