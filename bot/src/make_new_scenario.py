import os, sys, glob2
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


def make_new_scenario_request(request):

    print(request.POST)
    project_id = request.POST["project_id"]
    project_id = int(project_id)
    title = request.POST["title"]

    record_Project = Project.objects.get(id=project_id)

    record_Scenario = Scenario(
        project = record_Project,
        title = title
    )

    record_Scenario.save()