import os, sys

from django.conf.urls import include, url
from django.shortcuts import render
from . import views

# api
from board.src.load_save.load_pickle import load_pickle
from board.src.load_save.save_pickle import save_pickle


urlpatterns = [

    # 盤面の編集画面
    url(r"^$", views.board_page, name="board"),
    url(r"^[0-9]+$", views.board_page, name="board"),

    # 盤面保存
    url(r"^load_pickle$", load_pickle, name="load_pickle"),
    url(r"^save_pickle$", save_pickle, name="save_pickle"),

    # 動画生成
    # url(r"^movie/save$", views.board_page, name="board"),
]