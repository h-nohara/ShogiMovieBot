import os, sys

from django.conf.urls import include, url
from django.shortcuts import render
from . import views
from .views import new_account_page

# api
from accounts.src.account import when_login, create_new_account, overwrite_session_request, get_account_setting_request, change_account_setting_request
from accounts.src.project import get_projects_request, create_new_project_request, change_project_title_request, delete_project_request
from accounts.src.project.create_new_project_from_external_kifu import create_new_project_from_external_kifu_request

urlpatterns = [

    # account/

    # ログイン・ログアウトページ
    url(r"^login$", views.login_page, name="login"),
    url(r"^login/sp$", views.login_page_sp, name="login sp"),

    # ログイン処理
    url(r"^login/login$", when_login, name="when_login"),

    # セッション変数を登録
    url(r"^session/overwrite$", overwrite_session_request, name="overwrite_session_request"),

    # 新規アカウント作成ページ
    url(r"^new/$", new_account_page, name="new_account_page"),
    # 新規アカウント作成
    url(r"^new/create$", create_new_account, name="create_new_account"),

    # アカウント情報を取得
    url(r"^get$", get_account_setting_request, name="get_account_setting"),
    # アカウント情報を変更
    url(r"^change$", change_account_setting_request, name="change_account_setting"),
    

    # ホーム画面
    # url(r"^home/[-a-z0-9_]+$", views.home_page, name="home"),
    url(r"^home$", views.home_page, name="home"),
    url(r"^home/sp$", views.home_page_sp, name="home sp"),

    # プロジェクト一覧取得
    url(r"^project/get$", get_projects_request, name="get_projects"),

    # 棋譜の読み込みページ
    url(r"^project/from_WarsKifu$", views.new_project_from_WarsKifu_page, name="new_project_from_WarsKifu_page"),
    url(r"^project/from_WarsKifu/sp$", views.new_project_from_WarsKifu_page_sp, name="new_project_from_WarsKifu_page sp"),

    # プロジェクト新規作成
    url(r"^project/new$", create_new_project_request, name="create_new_project"),
    url(r"^project/create/from_WarsKifu$", create_new_project_from_external_kifu_request, name="create_new_project wars"),

    # プロジェクト名変更
    url(r"^project/change_title$", change_project_title_request, name="change project title"),

    # プロジェクト削除
    url(r"^project/delete$", delete_project_request, name="delete_project"),



    # テストページ

    # # ホーム画面future
    # url(r"^home/test_page$", views.home_page_future, name="home future"),

    # ホーム画面スマホ用テスト
    url(r"^sm/home/test_page$", views.test_home_page_sm, name="home sp test"),

]