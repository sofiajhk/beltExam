from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="login"),
    url(r'^register$', views.reg_process),
    url(r'^login$', views.log_process),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout, name="logout")
]
