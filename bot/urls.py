import os, sys

from django.conf.urls import include, url
from django.shortcuts import render
from . import views

# api
from bot.src.callback import callback


urlpatterns = [

    # /bot/

    # 
    # url(r"^$", views.board_page, name="board"),
    # url(r"^[0-9]+$", views.board_page, name="board"),

    # テスト
    url(r"^callback$", callback, name="callback"),
]