import os, sys

from django.conf.urls import include, url
from django.shortcuts import render
from . import views

# api

## book
from ShareShogi.src.contents.create.create_book import create_book_request
from ShareShogi.src.contents.get.get_latest_books import get_latest_books_request
from ShareShogi.src.contents.get.get_books import get_books_request

## chapter
from ShareShogi.src.contents.get.get_chapters import get_BookChapters_request
from ShareShogi.src.contents.create.create_chapter import create_chapter_request

## scene
from ShareShogi.src.contents.get.get_scenes import get_BookChaptersScenes_request

## transition
from ShareShogi.src.contents.transition.books_to_chapters import books_to_chapters_request


urlpatterns = [

    # ShareShogi/

    # ブック

    url(r"^books/page$", views.search_page, name="search page"),  # 検索画面
    url(r"^books/mypage$", views.myBook_page, name="my books page"),  # マイブック一覧画面
    url(r"^books/new$", views.newBook_page, name="my books page"),  # マイブック一覧画面
    url(r"^books/get-latests$", get_latest_books_request, name="search latests"),  # 最新のブックを取得
    url(r"^books/get-mine$", get_books_request, name="get my books"),  # 自分のブックを取得
    url(r"^books/create$", create_book_request, name="create book"),  # 新規ブック作成

    # url(r"^reader/search/exec$", views.search_page, name="exec search"),  # 検索結果を取得
    # url(r"^reader/book-info$", , name="get book info"),  # 本の内容を取得

    # チャプター

    url(r"^chapters/page$", views.chapters_page, name="chapters page"),  # チャプター一覧画面
    url(r"^chapters/mypage$", views.myChapters_page, name="my chapters page"),  # マイチャプター一覧画面
    url(r"^chapters/get$", get_BookChapters_request, name="get chapters"),
    url(r"^chapters/new$", views.newChapter_page, name="new chapter page"),  # 新規作成画面
    url(r"^chapters/create$", create_chapter_request, name="create chapter"),  # 新規作成

    # 各シーンのページ
    url(r"^scenes/page$", views.scene_page, name="scene page"),
    url(r"^scenes/get$", get_BookChaptersScenes_request, name="get scenes"),

    # アカウント

    url(r"^accounts/page$", views.account_page, name="account page"),  # アカウント設定画面
    url(r"^accounts/get$", views.account_page, name="account page"),  # アカウント設定を取得

    # セッション変数を保存してページ遷移

    url(r"^transition/books-to-chapters$", books_to_chapters_request, name="books to chapters"),  # ブック一覧画面から、チャプター一覧画面へ

]