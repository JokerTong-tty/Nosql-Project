# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 14:10
# @Author  : JokerTong
# @File    : urls.py
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('list_star', views.list_star, name='list_star'),
    path('star_doctor/<doctor_id>', views.star_doctor, name='star_doctor'),
    path('article/<id>', views.article, name='article'),

]
