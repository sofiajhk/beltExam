from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add$', views.add_process, name="add"),
    url(r'^edit/(?P<num>\d+)$', views.edit_process, name="edit"),
    url(r'^delete/(?P<num>\d+)$', views.delete, name="delete")
]
