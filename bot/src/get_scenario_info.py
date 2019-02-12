import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.project import Project
from bot.models.scenario import Scenario
from bot.models.message import Message
from bot.models.subscription import Subscription


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
    thumb_path = record_Scenario.thumb_path
    is_public = record_Scenario.is_public

    messages = get_messages(scenario_id)

    author = record_Scenario.project.user
    record_list_Subscription = Subscription.objects.filter(reader=author, author=author, scenario=record_Scenario, is_enabled=True)
    if len(record_list_Subscription) > 0:
        is_subsc = True
    else:
        is_subsc = False

    result = {
        "scenario_id" : scenario_id,
        "title" : title,
        "thumb_path" : thumb_path,
        "messages" : messages,
        "is_public" : is_public,
        "is_subscribing" : is_subsc
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

