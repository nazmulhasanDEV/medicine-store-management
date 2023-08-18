from django.contrib import admin
from django.urls import path, include, re_path
import uuid
from . import views

urlpatterns = [
    re_path(r'^index/$', views.index, name="index"),
    re_path(r'^$', views.dashboard, name="dashboard"),
]