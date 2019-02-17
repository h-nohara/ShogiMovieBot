import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.project import Project
from bot.models.scenario import Scenario
from board.models.movie import Movie

# api
from board.src.movie.get_movies import get_movies


@csrf_exempt
def get_movies_from_ScenarioId_request(request):

    print(request.POST)
    data = json.loads(request.body.decode("utf-8"))

    if "scenario_id" in data.keys():
        scenario_id = data["scenario_id"]
    else:
        scenario_id = request.session.get("scenario_id")
        
    scenario_id = int(scenario_id)
    movie_paths = get_movies_from_ScenarioId(scenario_id)

    result = {
        "code" : 200,
        "data" : {
            "paths" : movie_paths
        }
    }

    return JsonResponse(result)


def get_movies_from_ScenarioId(scenario_id):

    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_Project = record_Scenario.project
    
    paths = get_movies(record_Project.id)

    return paths