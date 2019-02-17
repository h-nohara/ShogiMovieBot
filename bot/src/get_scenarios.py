import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.user import User
from accounts.models.project import Project
from bot.models.scenario import Scenario
from bot.models.subscription import Subscription


@csrf_exempt
def get_scenarios_request(request):

    # print(request.POST)
    # data = json.loads(request.body.decode("utf-8"))
    # project_id = data["project_id"]
    # project_id = int(project_id)

    project_id = int(request.session.project_id)

    scenarios = get_scenarios(project_id)

    record_Project = Project.objects.get(id=project_id)
    project_title = record_Project.title
    
    result = {
        "code" : 200,
        "data" : {
            "scenarios" : scenarios,
            "project_title" : project_title
        }
    }

    return JsonResponse(result)


def get_scenarios(project_id):

    record_Project = Project.objects.get(id=project_id)
    record_list_Scenario = Scenario.objects.filter(project=record_Project)

    results = []

    for record_Scenario in record_list_Scenario:
        scenario_id = record_Scenario.id
        title = record_Scenario.title
        thumb_path  =record_Scenario.thumb_path
        info = {"scenario_id" : scenario_id, "title" : title, "thumb_path" : thumb_path}
        results.append(info)

    return results


@csrf_exempt
def get_public_scenarios_request(request):

    user_id = int(request.user.id)
    scenarios = get_public_scenarios(user_id=user_id)

    result = {
        "code" : 200,
        "data" : {
            "scenarios" : scenarios,
        }
    }

    return JsonResponse(result)


def get_public_scenarios(user_id):

    record_list_Scenario = Scenario.objects.filter(is_public=True)

    result = []

    for record_Scenario in record_list_Scenario:

        scenario_id = record_Scenario.id
        title = record_Scenario.title
        thumb_path  =record_Scenario.thumb_path

        record_User = User.objects.get(id=user_id)
        record_list_Subscription = Subscription.objects.filter(reader=record_User, scenario=record_Scenario, is_enabled=True)
        if len(record_list_Subscription) > 0:
            is_subscribing = True
        else:
            is_subscribing = False

        info = {
            "scenario_id" : scenario_id,
            "title" : title,
            "thumb_path" : thumb_path,
            "is_subscribing" : is_subscribing
        }
        result.append(info)

    return result