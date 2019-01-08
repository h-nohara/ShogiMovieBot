import os, sys

from django.conf.urls import include, url
from django.shortcuts import render

from .views import project_scenarios_page, scenario_editor_page

# api
from bot.src.callback import callback
from bot.src.create_new_account import create_new_account_request
from bot.src.get_scenarios import get_scenarios_request
from bot.src.get_scenario_info import get_scenario_info_request
from bot.src.create_new_scenario import create_new_scenario_request
from bot.src.delete_scenario import delete_scenario_request
from bot.src.get_movies_from_ScenarioId import get_movies_from_ScenarioId_request
from bot.src.update_messages import update_messages_request
from bot.src.transit import ScenarioEditor_to_ProjectScenarios_page, ScenarioEditor_to_Projects_page, Scenarios_to_Projects_page
from bot.src.distribute_now import distribute_now_request


urlpatterns = [

    # /bot/

    # 
    # url(r"^$", views.board_page, name="board"),
    # url(r"^[0-9]+$", views.board_page, name="board"),

    # ラインからのコールバック
    url(r"^callback$", callback, name="callback"),
    url(r"^callback/new_account$", create_new_account_request, name="callback_new_account"),

    # シナリオ一覧ページ
    url(r"^scenarios/[-a-z0-9_]+$", project_scenarios_page, name="project_scenarios_page"),
    # シナリオ編集ページ
    url(r"^scenario_editor/[-a-z0-9_]+$", scenario_editor_page, name="scenario_editor_page"),

    # ページを戻る
    url(r"^transit/ScenarioEditor_to_ProjectScenarios$", ScenarioEditor_to_ProjectScenarios_page, name="ScenarioEditor_to_ProjectScenarios"),
    url(r"^transit/ScenarioEditor_to_Projects$", ScenarioEditor_to_Projects_page, name="ScenarioEditor_to_Projects"),
    url(r"^transit/Scenarios_to_Projects$", Scenarios_to_Projects_page, name="Scenarios_to_Projects"),


    # シナリオ
    url(r"^scenario/get$", get_scenarios_request, name="get_scenarios"),  # シナリオ一覧
    url(r"^scenario/get_info$", get_scenario_info_request, name="get_scenario_info"),  # シナリオのタイトル等の情報と、メッセージ一覧
    url(r"^scenario/new$", create_new_scenario_request, name="create_new_scenario"),
    url(r"^scenario/delete$", delete_scenario_request, name="delete_scenario"),
    url(r"^scenario/movies$", get_movies_from_ScenarioId_request, name="get_movies_from_ScenarioId"),
    url(r"^scenario/update_messages$", update_messages_request, name="update_messages"),
    url(r"^scenario/distribute_now$", distribute_now_request, name="distribute_now"),
]