import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from ShareShogi.models.book import Book
from ShareShogi.models.chapter import Chapter
from ShareShogi.models.scene import Scene

# src


@csrf_exempt
def get_link_request(request):

    if request.method != "GET":
        return JsonResponse({"code" : 400})

    book_id = int(request.session["mybook_id"])

    link = "http://54.248.29.6:8000/ShareShogi/link/bookScenes" + str(book_id)

    return JsonResponse({"code" : 200, "link" : link})