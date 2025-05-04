# app1/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_person, name="create_person"),
    path("index/", views.index, name="index"),
]
