import os, sys, glob2
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.project import Project
from bot.models.scenario import Scenario


@csrf_exempt
def get_scenarios_request(request):

    print(request.POST)
    project_id = request.POST["project_id"]
    project_id = int(project_id)

    scenarios = get_scenarios(project_id)
    result = {
        "code" : 200,
        "data" : {
            "scenarios" : scenarios
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