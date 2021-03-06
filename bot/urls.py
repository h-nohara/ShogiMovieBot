import os, sys

from django.conf.urls import include, url
from django.shortcuts import render

from .views import project_scenarios_page, scenario_editor_page, public_scenarios_page, subscribing_scenarios_page
from . import views

# api
from bot.src.callback import callback
from bot.src.create_new_account import create_new_account_request
from bot.src.get_scenarios import get_scenarios_request, get_public_scenarios_request, get_subscribing_scenarios_request
from bot.src.get_scenario_info import get_scenario_info_request
# 新規プロジェクト
from bot.src.create_new_scenario import create_new_scenario_request
from bot.src.create_TsumeShogi_scenario import create_TsumeShogi_scenario_request

from bot.src.change_scenario_title import change_scenario_title_request
from bot.src.delete_scenario import delete_scenario_request
from bot.src.get_movies_from_ScenarioId import get_movies_from_ScenarioId_request
from bot.src.update_messages import update_messages_request
from bot.src.transit import ScenarioEditor_to_ProjectScenarios_page, ScenarioEditor_to_Projects_page, Scenarios_to_Projects_page, Board_to_ProjectScenarios_page
from bot.src.distribute_now import distribute_now_request
from bot.src.regular_distribution import regular_distribution_request, test_regular_distribution_request
from bot.src.change_subscription_setting import change_subscription_setting_request
from bot.src.change_public_setting import change_public_setting_request


urlpatterns = [

    # /bot/

    # url(r"^$", views.board_page, name="board"),
    # url(r"^[0-9]+$", views.board_page, name="board"),

    # ラインからのコールバック
    url(r"^callback$", callback, name="callback"),
    url(r"^callback/new_account$", create_new_account_request, name="callback_new_account"),

    # シナリオ一覧ページ
    # url(r"^scenarios/[-a-z0-9_]+$", project_scenarios_page, name="project_scenarios_page_old"),
    url(r"^scenarios$", project_scenarios_page, name="project_scenarios_page"),
    url(r"^scenarios/sp$", views.project_scenarios_page_sp, name="project_scenarios_page sp"),

    # シナリオ編集ページ
    # url(r"^scenario_editor/[-a-z0-9_]+$", scenario_editor_page, name="scenario_editor_page_old"),
    url(r"^scenario_editor$", scenario_editor_page, name="scenario_editor_page"),
    url(r"^scenario_editor/sp$", views.scenario_editor_page_sp, name="scenario_editor_page sp"),

    # 公開されているシナリオの一覧ページ
    url(r"^scenarios/public$", public_scenarios_page, name="public_scenarios_page"),
    url(r"^scenarios/public/sp$", views.public_scenarios_page_sp, name="public_scenarios_page sp"),

    # 購読しているシナリオの一覧ページ
    url(r"^scenarios/subscribing$", subscribing_scenarios_page, name="subscribing_scenarios_page"),
    url(r"^scenarios/subscribing/sp$", views.subscribing_scenarios_page_sp, name="subscribing_scenarios_page sp"),

    url(r"^scenario/subscribing/get$", get_subscribing_scenarios_request, name="get_subscribing"),

    # ページを戻る
    url(r"^transit/ScenarioEditor_to_ProjectScenarios$", ScenarioEditor_to_ProjectScenarios_page, name="ScenarioEditor_to_ProjectScenarios"),
    url(r"^transit/ScenarioEditor_to_Projects$", ScenarioEditor_to_Projects_page, name="ScenarioEditor_to_Projects"),
    url(r"^transit/Scenarios_to_Projects$", Scenarios_to_Projects_page, name="Scenarios_to_Projects"),
    url(r"^transit/Board_to_Scenarios$", Board_to_ProjectScenarios_page, name="Board_to_ProjectScenarios"),


    # シナリオ
    url(r"^scenario/get$", get_scenarios_request, name="get_scenarios"),  # シナリオ一覧
    url(r"^scenario/get_public$", get_public_scenarios_request, name="get_public_scenarios"),  # 公開されているシナリオ一覧
    url(r"^scenario/get_info$", get_scenario_info_request, name="get_scenario_info"),  # シナリオのタイトル等の情報と、メッセージ一覧
    # 新規プロジェクト作成
    url(r"^scenario/new$", create_new_scenario_request, name="create_new_scenario"),  # 通常
    url(r"^scenario/TsumeShogi/new$", create_TsumeShogi_scenario_request, name="create_new_TsumeShogi_scenario"),  # 詰将棋シナリオ

    url(r"^scenario/change_title$", change_scenario_title_request, name="change_scenario_title"),
    url(r"^scenario/delete$", delete_scenario_request, name="delete_scenario"),
    url(r"^scenario/movies$", get_movies_from_ScenarioId_request, name="get_movies_from_ScenarioId"),
    url(r"^scenario/update_messages$", update_messages_request, name="update_messages"),
    url(r"^scenario/distribute_now$", distribute_now_request, name="distribute_now"),
    url(r"^scenario/change_subscription_setting$", change_subscription_setting_request, name="change_subscription_setting"),
    url(r"^scenario/change_public_setting$", change_public_setting_request, name="change_public_setting"),
    url(r"^scenario/regular_distribution$", regular_distribution_request, name="regular_dist"),
    url(r"^scenario/regular_distribution/test$", test_regular_distribution_request, name="test_regular_dist"),


    # テストページ

    url(r"^sm/scenarios/test_page$", views.test_project_scenarios_page_sm, name="project_scenarios_page sm"),
    url(r"^sm/scenario_editor/test_page$", views.test_scenario_editor_page_sm, name="scenario_editor_page sm"),
    url(r"^sm/scenarios/public/test_page$", views.test_public_scenarios_page_sm, name="public_scenarios_page sm"),
    url(r"^sm/scenarios/subscribing/test_page$", views.test_subscribing_scenarios_page_sm, name="subscribing_scenarios_page sm"),

]