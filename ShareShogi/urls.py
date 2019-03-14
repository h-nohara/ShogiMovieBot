import os, sys

from django.conf.urls import include, url
from django.shortcuts import render
from . import views
from .views import new_account_page

# api
from ShareShogi.src.contents.create.create_book import create_book_request

urlpatterns = [

    # ShareShogi/

    # 検索ページ
    url(r"^reader/search$", views.search_page, name="search page"),

    url(r"^reader/search/exec$", views.search_page, name="exec search"),  # 検索結果を取得
    # url(r"^reader/book-info$", , name="get book info"),  # 本の内容を取得

    # チャプター一覧ページ
    url(r"^reader/chapters$", views.chapters_page, name="chapter page"),

    # 各シーンのページ
    url(r"^reader/scene$", views.scene_page, name="scene page"),

    # 新規ブック作成
    url(r"^create/book$", create_book_request, name="create book"),

]