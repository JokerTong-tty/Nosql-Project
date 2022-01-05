# -*- coding: utf-8 -*-
# @Time    : 2021/6/18 15:15
# @Author  : JokerTong
# @File    : urls.py
from django.urls import path
from . import views

app_name = 'answer'
urlpatterns = [
    path('get_answer/<question>', views.get_answer, name='get_answer'),
    path('chat/', views.chat, name='chat'),
]
