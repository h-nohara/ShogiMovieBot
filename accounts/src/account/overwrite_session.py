
import os, sys
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt



@login_required(login_url="/account/login")
@csrf_exempt
def overwrite_session_request(request):

    data = json.loads(request.body.decode("utf-8"))
    keys = data.keys()

    if "project_id" in keys:
        project_id = int(data["project_id"])
        request.session["project_id"] = project_id
        print("")
        print("プロジェクトodを保存しました")
        print("")

    elif "scenario_id" in keys:
        scenario_id = int(data["scenario_id"])
        request.session["scenario_id"] = scenario_id

    return JsonResponse({"code" : 200})