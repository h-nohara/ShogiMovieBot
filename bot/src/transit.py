import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.user import User
from accounts.models.project import Project
from bot.models.scenario import Scenario


# シナリオ編集ページからの移動

@csrf_exempt
def ScenarioEditor_to_ProjectScenarios_page(request):

    data = json.loads(request.body.decode("utf-8"))
    scenario_id = data["scenario_id"]
    scenario_id = int(scenario_id)

    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_Project = record_Scenario.project
    project_id = record_Project.id
    project_id = str(project_id)

    return redirect("/bot/scenarios/{}".format(project_id))


@csrf_exempt
def ScenarioEditor_to_Projects_page(request):
    
    data = json.loads(request.body.decode("utf-8"))
    scenario_id = data["scenario_id"]
    scenario_id = int(scenario_id)

    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_Project = record_Scenario.project
    record_User = record_Project.user

    user_id = record_User.id
    user_id = str(user_id)

    return redirect("/account/home/{}".format(user_id))


# シナリオ一覧ページからの移動

@csrf_exempt
def Scenarios_to_Projects_page(request):
    
    data = json.loads(request.body.decode("utf-8"))
    project_id = data["project_id"]
    project_id = int(project_id)

    record_Project = Project.objects.get(id=project_id)
    record_User = record_Project.user

    user_id = record_User.id
    user_id = str(user_id)

    the_url = "/account/home/{}".format(user_id)
    return JsonResponse({"code" : 200, "data" : {"url" : the_url}})

    # return redirect("/account/home/{}".format(user_id))