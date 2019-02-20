import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.project import Project
from bot.models.scenario import Scenario
from bot.models.message import Message

# api
from accounts.src.utils.generate_fname import generate_basename
from board.src.movie.generate_InitBoard_image import generate_InitBoard_image


@csrf_exempt
def create_TsumeShogi_scenario_request(request):
    
    project_id = int(request.session.get("project_id"))

    record_Project = Project.objects.get(id=project_id)
    title = "新規詰将棋シナリオ"

    # 画像を生成
    path_cloud = generate_InitBoard_image(project_id=project_id)


    # 新規シナリオを作成

    record_Scenario = Scenario(
        project = record_Project,
        title = title
    )
    record_Scenario.save()

    # メッセージ一覧を作成

    messages = [
        Message(scenario=record_Scenario, kind="text", text="今日の詰将棋の問題です"),
        Message(scenario=record_Scenario, kind="image", image_path=path_cloud)
    ]

    for record_Message in messages:
        record_Message.save()

    return JsonResponse({"code" : 200})