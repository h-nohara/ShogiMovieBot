import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project


@csrf_exempt
def change_project_title_request(request):

    data = json.loads(request.body.decode("utf-8"))
    print(data)
    project_id = data["project_id"]
    project_id = int(project_id)
    title = data["title"]

    record_Project = Project.objects.get(id=project_id)
    record_Project.title = title
    record_Project.save()

    json_response = {
        "code" : 200
    }

    return JsonResponse(json_response)
