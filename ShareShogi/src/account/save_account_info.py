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
def save_account_info_request(request):

    payload = json.loads(request.body.decode("utf-8"))

    record_User = request.user

    record_User.username = payload["username"]
    record_User.nickname = payload["nickname"]

    record_User.save()

    return JsonResponse({"code" : 200})
