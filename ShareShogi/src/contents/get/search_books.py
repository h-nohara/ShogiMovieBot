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
def get_user_books_request(request):

    '''
    特定のユーザのブック一覧を取得する
    '''

    if request.method == "POST":
        payload = request.POST

    else:
        raise("only POST accept")

    opening_sente = payload["opening_sente"]
    opening_gote = payload["opening_gote"]


    # # bookの情報を取得する
    # books = get_books(user_id)

    # result = {
    #     "code" : 200,
    #     "result": books
    # }
    
    # return JsonResponse(result)


