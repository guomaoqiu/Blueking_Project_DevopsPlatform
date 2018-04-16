# -*- coding: utf-8 -*-

from django.conf.urls import url

from account import views

urlpatterns = [
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^check_failed/$', views.check_failed, name='check_failed'),  # 权限验证错误页面
]
