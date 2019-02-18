import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project
from board.models.movie import Movie


def get_movies(project_id):

    record_Project = Project.objects.get(id=project_id)
    concat_movie_path = record_Project.concat_movie_path

    record_list_Movie = Movie.objects.filter(project=record_Project)

    # basenames = [record_Movie.basename for record_Movie in record_list_Movie]
    paths = [record_Movie.path for record_Movie in record_list_Movie]
    paths.append(concat_movie_path)

    return paths


@csrf_exempt
def get_movies_request(request):

    print("[start get movies")

    # payload = json.loads(request.body.decode("utf-8"))
    # project_id = payload["project_id"]
    # project_id = int(project_id)

    if request.method == "GET":
        project_id = int(request.session.get("project_id"))
    else:
        raise ValueError("only GET receive")

    paths = get_movies(project_id)

    json_response = {
        "code" : 200,
        "result" : {
            "paths" : paths
        }
    }

    print(json_response)
    print("success : get movies]")

    return JsonResponse(json_response)