import os, sys

from django.conf.urls import include, url
from django.shortcuts import render
from . import views
from .views import new_account_page

# api
from accounts.src.account import when_login, create_new_account
from accounts.src.project import get_projects_request, create_new_project_request, change_project_title_request

urlpatterns = [

    # account/

    # ログイン・ログアウトページ
    url(r"^login$", views.login_page, name="login"),
    # ログイン・ログアウトページ
    url(r"^login/login$", when_login, name="when_login"),

    # 新規アカウント作成
    url(r"^new/$", new_account_page, name="new_account_page"),
    # 新規アカウント作成
    url(r"^new/create$", create_new_account, name="create_new_account"),

    # ホーム画面
    url(r"^home/[-a-z0-9_]+$", views.home_page, name="home"),
    # プロジェクト一覧取得
    url(r"^project/get$", get_projects_request, name="get_projects_request"),
    # プロジェクト新規作成
    url(r"^project/new$", create_new_project_request, name="create_new_project_request"),
    # プロジェクト名変更
    url(r"^project/change_title$", change_project_title_request, name="change project title"),

]