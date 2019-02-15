import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project

def get_projects(record_User):

    record_list_Project = Project.objects.filter(user=record_User)
    record_list_Project = record_list_Project[::-1]

    projects = []

    for record_Project in record_list_Project:

        project_id = record_Project.id
        title = record_Project.title
        pickle_basename = record_Project.pickle_basename
        pickle_path = record_Project.pickle_path
        concat_movie_path = record_Project.concat_movie_path

        info = {
            "project_id" : project_id,
            "title" : title,
            "pickle_path" : pickle_path,
            "pickle_basename" : pickle_basename,
            "concat_movie_path" : concat_movie_path
        }

        projects.append(info)

    
    return projects


@csrf_exempt
def get_projects_request(request):

    # payload = json.loads(request.body.decode("utf-8"))
    # user_id = payload["user_id"]
    # user_id = int(user_id)
    user_id = request.user.id

    record_User = User.objects.get(id=user_id)
    projects = get_projects(record_User)

    json_response = {
        "code" : 200 ,
        "data" : {
            "projects" : projects,
        }
    }

    return JsonResponse(json_response)