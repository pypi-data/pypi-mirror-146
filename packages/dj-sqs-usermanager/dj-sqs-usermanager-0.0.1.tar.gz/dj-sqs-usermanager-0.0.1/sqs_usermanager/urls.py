from distutils.version import (
    StrictVersion,
)  # pylint: disable=no-name-in-module,import-error

from django import get_version
from django.urls import re_path as pattern

from . import views

urlpatterns = [
    pattern(r"^notification_queue/$", views.notification_about_queue),
]

app_name = "notifications"
