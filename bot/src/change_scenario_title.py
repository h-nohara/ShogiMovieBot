import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from bot.models.scenario import Scenario


@csrf_exempt
def change_scenario_title_request(request):

    # receive
    print(request.POST)
    data = json.loads(request.body.decode("utf-8"))
    scenario_id = data["scenario_id"]
    scenario_id = int(scenario_id)
    title = data["title"]

    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_Scenario.title = title
    record_Scenario.save()

    return JsonResponse({"code" : 200})