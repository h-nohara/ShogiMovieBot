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
def new_from_preview_request(request):

    '''
    プレビュー画面から、新規シーン作成ページへ
    '''

    # idを記録しておく

    if request.method == "POST":

        payload = json.loads(request.body.decode("utf-8"))

        request.session["activeSection_index"] = int(payload["activeSection_index"])
        request.session["activeSection_id"] = int(payload["activeSection_id"])
        request.session["activeSlide_index"] = int(payload["activeSlide_index"])
        request.session["activeSlide_id"] = int(payload["activeSlide_id"])
        request.session["is_create_next"] = int(payload["is_create_next"])

    else:
        return JsonResponse({"code" : 400, "comment" : "POSTで送ってください"})

    result = {
        "code" : 200,
    }

    return JsonResponse(result)
    