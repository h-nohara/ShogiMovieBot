import os, sys
import json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt


# api
from accounts.src.project import get_projects

# db
from accounts.models.user import User


@csrf_exempt
def when_login(request):

    data = json.loads(request.body.decode("utf-8"))
    username = data["username"]
    password = data["password"]

    user = authenticate(username=username, password=password)

    if user is not None:
        
        # record_User = User.objects.get(username=username)
        # user_id = record_User.id

        # ログイン処理
        login(request, user)

        return JsonResponse({"code" : 200})

    else:
        return JsonResponse({"code" : 400, "error_message" : "ログイン情報が間違っています"})
    
    # return render(request, "accounts/home.html")
