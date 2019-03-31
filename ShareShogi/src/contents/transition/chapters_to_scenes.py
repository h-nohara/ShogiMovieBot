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
def chapters_to_scenes_request(request):

    '''
    チャプター一覧画面から、シーン一覧画面へ遷移
    '''

    # chapter_idを記録しておく

    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))
        chapter_id = int(payload["chapter_id"])
        is_mine = payload["is_mine"]

    else:
        return JsonResponse({"code" : 400, "comment" : "POSTで送ってください"})

    if is_mine:
        request.session["mychapter_id"] = chapter_id
    else:
        request.session["chapter_id"] = chapter_id


    dest_url = "/ShareShogi/scenes/mypage"

    result = {
        "code" : 200,
        "result": dest_url
    }

    return JsonResponse(result)

    # return redirect(dest_url)

    