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
def link_to_scenes_request(request):

    '''
    リンクからシーン一覧へ
    '''

    # book_idを記録しておく

    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))
        book_id = int(payload["book_id"])

    else:
        return JsonResponse({"code" : 400, "comment" : "POSTで送ってください"})
    
    request.session["book_id"] = book_id


    return render(request, "ShareShogi/scenes.html")

    dest_url = "/ShareShogi/scenes/page"

    # result = {
    #     "code" : 200,
    #     "result": dest_url
    # }

    # return JsonResponse(result)

    # return redirect(dest_url)

    