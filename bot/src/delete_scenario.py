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


def delete_scenario_request(request):

    # receive
    print(request.POST)
    data = json.loads(request.body.decode("utf-8"))
    scenario_id = data["scenario_id"]
    scenario_id = int(scenario_id)

    # delete
    delete_scenario(scenario_id)

    return JsonResponse({"code" : 200})


def delete_scenario(scenario_id):

    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_list_Message = Message.objects.filter(scenario=record_Scenario)

    for record_Message in record_list_Message:
        record_Message.delete()