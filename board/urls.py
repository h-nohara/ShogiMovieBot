import os, sys

from django.conf.urls import include, url
from django.shortcuts import render
from . import views

# api
from board.src.load_save.load_pickle import load_pickle
from board.src.load_save.save_pickle import save_pickle
from board.src.movie import get_movies_request, generate_movies
from board.src.load_save.save_initial_board import save_initial_board_request


urlpatterns = [

    # /board/

    # 盤面の編集画面
    url(r"^editor$", views.board_page, name="board"),
    # url(r"^[0-9]+$", views.board_page, name="board"),
    url(r"^editor/sp$", views.board_page_sp, name="board sp"),

    # 開始盤面の編集画面
    url(r"^initial/editor$", views.initial_board_page, name="board"),
    url(r"^initial/editor/sp$", views.initial_board_page_sp, name="board sp"),

    url(r"^initial/editor/save$", save_initial_board_request, name="save initial board"),

    # 盤面読み込み・保存
    url(r"^load_pickle$", load_pickle, name="load_pickle"),
    url(r"^save_pickle$", save_pickle, name="save_pickle"),

    # 動画
    url(r"^movie/get$", get_movies_request, name="get_movies"),
    url(r"^movie/generate$", generate_movies, name="generate_movies"),


    # テストページ

    url(r"^sm/test_page$", views.test_board_page_sm, name="board"),
    url(r"^sm/initial/editor/test_page$", views.test_initial_board_page_sm, name="board"),
]