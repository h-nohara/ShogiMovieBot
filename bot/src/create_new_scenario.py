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


@csrf_exempt
def create_new_scenario_request(request):

    print(request.POST)
    data = json.loads(request.body.decode("utf-8"))
    
    project_id = int(request.session.get("project_id"))
    title = data["title"]

    record_Project = Project.objects.get(id=project_id)

    record_Scenario = Scenario(
        project = record_Project,
        title = title
    )

    record_Scenario.save()

    return JsonResponse({"code" : 200})