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
def books_to_chapters_request(request):

    '''
    ブック一覧画面から、チャプター一覧画面へ遷移
    '''

    # book_idを記録しておく

    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))
        book_id = int(payload["book_id"])

    else:
        return JsonResponse({"code" : 400, "comment" : "POSTで送ってください"})

    request.session["book_id"] = book_id


    dest_url = "/ShareShogi/chapters/mypage"

    result = {
        "code" : 200,
        "result": dest_url
    }

    return JsonResponse(result)

    # return redirect(dest_url)

    