import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from ShareShogi.models.book import Book
from ShareShogi.models.chapter import Chapter
from ShareShogi.models.scene import Scene


@csrf_exempt
def create_new_account_ForAdmin_request(request):

    if not request.user.is_superuser:
        return JsonResponse({"code" : 400})

    payload = json.loads(request.body.decode("utf-8"))

    username = payload["username"]
    password = payload["password"]

    record_User = User(
        is_superuser = False,
        is_staff = False,
        username = username
    )

    record_User.set_password(password)
    record_User.save()

    return JsonResponse({"code" : 200})
