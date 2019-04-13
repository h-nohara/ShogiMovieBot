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
def save_book_info_request(request):

    '''
    ブック情報を更新
    '''

    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))

    else:
        return JsonResponse({"code" : 400})

    title = payload["title"]
    is_public = payload["is_public"]
    if is_public:
        is_public = True
    else:
        is_public = False

    book_id = int(request.session["mybook_id"])
    record_Book = Book.objects.get(id=book_id)

    record_Book.title = title
    record_Book.is_public = is_public

    record_Book.save()

    return JsonResponse({"code" : 200})