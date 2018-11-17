import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project
from board.models.movie import Movie


def get_movies(record_Project):

    record_list_Movie = Movie.objects.filter(project=record_Project)

    basenames = [record_Movie.basename for record_Movie in record_list_Movie]
    paths = [record_Movie.path for record_Movie in record_list_Movie]

    return paths



def get_movies_request(request):

    data = json.loads(request.body.decode("utf-8"))
    project_id = data["project_id"]
    project_id = int(project_id)

    record_Project = Project.objects.get(id=project_id)

    paths = get_movies(record_Project)

    json_response = {
        "code" : 200,
        "result" : {
            "paths" : paths
        }
    }

    return JsonResponse(json_response)


# pickle_basename = record_Project.pickle_basename
# key = pickle_basename.split(".")[0]


