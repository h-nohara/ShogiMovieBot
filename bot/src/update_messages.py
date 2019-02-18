import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.project import Project
from bot.models.scenario import Scenario
from bot.models.message import Message


@csrf_exempt
def update_messages_request(request):

    data = json.loads(request.body.decode("utf-8"))
    messages = data["messages"]
    scenario_id = int(request.session.get("scenario_id"))

    update_messages(scenario_id=scenario_id, messages=messages)

    return JsonResponse({"code" : 200})


def update_messages(scenario_id, messages):

    record_Scenario = Scenario.objects.get(id=scenario_id)

    # 元々のものを削除
    record_list_Message = Message.objects.filter(scenario=record_Scenario)
    for record_Message in record_list_Message:
        record_Message.delete()

    # 新たに登録
    for info in messages:
        kind = info["kind"]

        if kind == "text":
            record_Message = Message(
                scenario = record_Scenario,
                kind = "text",
                text = info["text"]
            )

        elif kind == "movie":
            record_Message = Message(
                scenario = record_Scenario,
                kind = "movie",
                movie_path = info["movie_path"]
            )

        record_Message.save()