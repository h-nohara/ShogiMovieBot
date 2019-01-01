import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.user import User
from accounts.models.project import Project
from bot.models.scenario import Scenario
from bot.models.message import Message

# api
from bot.src.line_bot_api import line_bot_api, push_text_message, nohara_first_id


# シナリオを今すぐ配信

@csrf_exempt
def distribute_now_request(request):

    data = json.loads(request.body.decode("utf-8"))
    scenario_id = data["scenario_id"]
    scenario_id = int(scenario_id)

    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_Project = record_Scenario.project
    record_User = record_Project.user
    user_id = record_User.id

    distribute(scenario_id=scenario_id, user_id=user_id)

    return JsonResponse({"code" : 200})



def distribute(scenario_id, user_id):

    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_User = User.objects.get(id=user_id)
    line_id = record_User.line_id

    # テスト
    line_id = nohara_first_id

    record_list_Message = Message.objects.filter(scenario=record_Scenario)

    for record_Message in record_list_Message:

        kind = record_Message.kind
        is_stop = record_Message.is_stop

        if kind == "text":
            text = record_Message.text
            push_text_message(text=text, line_id=line_id)

        elif kind == "movie":
            movie_path = record_Message.movie_path
            push_text_message(text=movie_path, line_id=line_id)