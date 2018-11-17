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

    projects_info = []

    for record_Project in record_list_Project:

        id_ = record_Project.id
        title = record_Project.title
        pickle_path = record_Project.pickle_path
        concat_movie_path = record_Project.concat_movie_path

        info = {
            "id" : id_,
            "title" : title,
            "pickle_path" : pickle_path,
            "concat_movie_path" : concat_movie_path
        }

        projects_info.append(info)

    
    return projects_info


@csrf_exempt
def get_projects_request(request):

    data = json.loads(request.body.decode("utf-8"))
    print(data)
    user_id = data["user_id"]
    user_id = int(user_id)

    record_User = User.objects.get(id=user_id)
    projects_info = get_projects(record_User)

    json_response = {
        "code" : 200 ,
        "result" : {
            "projects_info" : projects_info,
        }
    }

    return JsonResponse(json_response)