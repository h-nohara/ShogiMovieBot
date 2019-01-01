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
def get_scenario_info_request(request):

    '''
    シナリオのタイトル等の情報と、メッセージ一覧を渡す
    '''

    print(request.POST)
    data = json.loads(request.body.decode("utf-8"))
    scenario_id = data["scenario_id"]
    scenario_id = int(scenario_id)

    scenario_info = get_scenario_info(scenario_id)

    result = {
        "code" : 200,
        "data" : scenario_info
    }

    return JsonResponse(result)


def get_scenario_info(scenario_id):

    record_Scenario = Scenario.objects.get(id=scenario_id)
    title = record_Scenario.title
    thumb_path  =record_Scenario.thumb_path

    messages = get_messages(scenario_id)

    result = {
        "scenario_id" : scenario_id,
        "title" : title,
        "thumb_path" : thumb_path,
        "messages" : messages
    }

    return result


def get_messages(scenario_id):

    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_list_Message = Message.objects.filter(scenario=record_Scenario)

    messages = []

    for record_Message in record_list_Message:

        info = {
            "message_id" : record_Message.id,
            "kind" : record_Message.kind,
            "text" : record_Message.text,
            "image_path" : record_Message.image_path,
            "movie_path" : record_Message.movie_path,
            "is_stop" : record_Message.is_stop
        }

        messages.append(info)

    return messages

