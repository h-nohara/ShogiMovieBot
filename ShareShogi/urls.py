import os, sys

from django.conf.urls import include, url
from django.shortcuts import render
from . import views

# api

## account
from ShareShogi.src.account.login_ShareShogi import login_ShareShogi_request
from ShareShogi.src.account.get_account_info import get_account_info_request
from ShareShogi.src.account.save_account_info import save_account_info_request
from ShareShogi.src.account.create_new_account_ForAdmin import create_new_account_ForAdmin_request

## book
from ShareShogi.src.contents.create.create_book import create_book_request
from ShareShogi.src.contents.get.get_latest_books import get_latest_books_request
from ShareShogi.src.contents.get.get_books import get_user_books_request
from ShareShogi.src.contents.get.get_book_info import get_book_info_request
from ShareShogi.src.contents.delete.delete_book import delete_book_request
from ShareShogi.src.contents.save.save_book_info import save_book_info_request

## chapter
from ShareShogi.src.contents.get.get_chapters import get_BookChapters_request, get_BookChapters_sample_request
from ShareShogi.src.contents.create.create_chapter import create_chapter_request
from ShareShogi.src.contents.delete.delete_chapter import delete_chapter_request

## scene
from ShareShogi.src.contents.get.get_scenes import get_BookChaptersScenes_request
from ShareShogi.src.contents.create.create_scene_from_preview import create_scene_from_preview_request
from ShareShogi.src.contents.delete.delete_scene import delete_scene_request

## transition
from ShareShogi.src.contents.transition.books_to_chapters import books_to_chapters_request
from ShareShogi.src.contents.transition.chapters_to_scenes import chapters_to_scenes_request
from ShareShogi.src.contents.transition.new_from_preview import new_from_preview_request

# 次の一手
from ShareShogi.src.contents.create.create_NextItte import create_nextItte_request
from ShareShogi.src.contents.get.get_NextItte import get_user_NextItte_request, get_NextItte_request

# link
from ShareShogi.src.contents.get.get_link import get_link_request


urlpatterns = [

    # ShareShogi/

    # ブック

    url(r"^books/search$", views.search_page, name="search page"),  # 検索画面
    url(r"^books/mypage$", views.myBook_page, name="my books page"),  # マイブック一覧画面
    url(r"^books/new$", views.newBook_page, name="my books page"),  # マイブック一覧画面
    url(r"^books/infoEditor$", views.bookEditor_page, name="my book editor"),  # ブック情報編集
    url(r"^books/get-latests$", get_latest_books_request, name="search latests"),  # 最新のブックを取得
    url(r"^books/get-mine$", get_user_books_request, name="get my books"),  # 自分のブックを取得
    url(r"^books/api/create$", create_book_request, name="create book"),  # 新規ブック作成
    url(r"^books/api/get-info$", get_book_info_request, name="get book info"),  # ブック情報を取得
    url(r"^books/api/delete$", delete_book_request, name="delete book"),  # ブックを削除
    url(r"^books/api/save$", save_book_info_request, name="save book"),  # ブック情報を更新

    # url(r"^reader/search/exec$", views.search_page, name="exec search"),  # 検索結果を取得
    # url(r"^reader/book-info$", , name="get book info"),  # 本の内容を取得

    # チャプター

    url(r"^chapters/page$", views.chapters_page, name="chapters page"),  # チャプター一覧画面
    url(r"^chapters/mypage$", views.myChapters_page, name="my chapters page"),  # マイチャプター一覧画面
    url(r"^chapters/get$", get_BookChapters_request, name="get chapters"),
    url(r"^chapters/new$", views.newChapter_page, name="new chapter page"),  # 新規作成画面
    url(r"^chapters/api/create$", create_chapter_request, name="create chapter"),  # 新規作成
    # url(r"^chapters/api/create_from_preview$", create_chapter_request, name="create from preview"),  ######## プレビューから新規作成
    url(r"^chapters/api/delete$", delete_chapter_request, name="delete chapter"),  # 削除

    # シーン

    url(r"^scenes/page$", views.scene_page, name="scenes page"),
    url(r"^scenes/mypage$", views.myScenes_page, name="my scenes page"),
    url(r"^scenes/get$", get_BookChaptersScenes_request, name="get scenes"),
    url(r"^scenes/new$", views.newScene_page, name="new scene page"),  # 新規作成画面
    url(r"^scenes/api/create_from_preview$", create_scene_from_preview_request, name="create scene from preview"),
    url(r"^scenes/api/delete$", delete_scene_request, name="delete scene"),

    url(r"^scenes/demopage1$", views.scene_demopage1, name="scenes page demo1"),  # デモページ

    url(r"^scenes/testUpload$", views.testUpload_page, name="test upload"),

    # アカウント

    url(r"^accounts/mypage$", views.account_page, name="account page"),  # アカウント設定画面
    url(r"^accounts/api/get$", get_account_info_request, name="get account"),  # アカウント設定を取得
    url(r"^accounts/api/save$", save_account_info_request, name="save account"),  # アカウント設定を更新
    url(r"^accounts/loginpage$", views.login_page, name="login page"),  # ログインページ
    url(r"^accounts/newForAdmin$", views.newAccountForAdmin_page, name="new account for admin page"),  # 新規アカウント作成ページ（管理者向け）
    url(r"^accounts/api/login$", login_ShareShogi_request, name="get account"),  # ログイン
    url(r"^accounts/api/createByAdmin$", create_new_account_ForAdmin_request, name="create new account for admin"),  # 新規アカウント作成（管理者向け）

    # セッション変数を保存してページ遷移

    url(r"^transition/books-to-chapters$", books_to_chapters_request, name="books to chapters"),
    url(r"^transition/chapters-to-scenes$", chapters_to_scenes_request, name="chapters to scenes"),
    url(r"^transition/new_from_preview$", new_from_preview_request, name="preview to new page"),
    # url(r"^transition/link-to-scenes$", new_from_preview_request, name="link to scene"),


    # 次の一手
    url(r"^nextItte/api/create$", create_nextItte_request, name="create nextItte"),
    url(r"^nextItte/api/get/user$", get_user_NextItte_request, name="get user's nextItte"),
    url(r"^nextItte/api/get/filter$", get_NextItte_request, name="filter nextItte"),


    # リンクから閲覧

    url(r"^link/bookScenes[0-9]+$", views.scene_page, name="scenes page"),
    # url(r"^link/api/get$", views.scene_page, name="scenes page"),
    url(r"^link/api/get-mine$", get_link_request, name="get mybook link"),

]