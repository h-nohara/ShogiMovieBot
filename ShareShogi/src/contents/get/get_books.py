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
def get_books_request(request):

    '''
    特定のユーザのブック一覧を取得する
    '''

    # user_idを取得する
    if request.method == "GET":
        user_id = int(request.user.id)

    elif request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))
        user_id = int(payload["user_id"])

    # bookの情報を取得する
    books = get_books(user_id)

    result = {
        "code" : 200,
        "result": books
    }
    
    return JsonResponse(result)


def get_books(user_id):

    '''
    特定のユーザのブック一覧を取得する
    '''

    record_User = User.objects.get(id=user_id)
    queryset_Book = Book.objects.filter(user=record_User)

    books = []

    for record_Book in queryset_Book:

        book_info = get_book_info(book_id=int(record_Book.id))
        books.append(book_info)

    return books


def get_book_info(book_id):
    
    '''
    特定のブックに関する情報を取得する
    
    get_childs : Trueなら、ブックに属する全てのチャプター情報も加える
    '''

    record_Book = Book.objects.get(id=book_id)

    book_info = {
        "book_id" : book_id,
        "nickname" : record_Book.user.nickname,
        "title" : record_Book.title,
        "thumb_url" : record_Book.thumb_url,
        "is_public" : record_Book.is_public,
        "opening_sente" : record_Book.opening_sente,
        "opening_gote" : record_Book.opening_gote,
    }

    return book_info