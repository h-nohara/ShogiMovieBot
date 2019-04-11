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
def get_BookChapters_request(request):

    # book_idを取得する

    if request.method == "GET":
        if "mybook_id" in request.session:
            book_id = int(request.session["mybook_id"])
        else:
            return JsonResponse({"code" : 400})

    elif request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))
        book_id = int(payload["book_id"])

    # else:
    #     return JsonResponse({"code" : 400})

    # ブック情報を取得
    record_Book = Book.objects.get(id=book_id)

    # チャプター一覧を取得する
    chapters = get_chapters(book_id=book_id)

    BookChapters = {
        "book_id" : book_id,
        "book_title" : record_Book.title,
        "publisher" : record_Book.user.nickname,
        "chapters" : chapters
    }

    result = {
        "code" : 200,
        "result": BookChapters
    }
    
    return JsonResponse(result)


def get_chapters(book_id):
    
    '''
    チャプター一覧を取得する
    '''

    chapters = []

    queryset_Chapter = Chapter.objects.filter(book=book_id)

    for record_Chapter in queryset_Chapter:

        chapter_info = {
            "chapter_id" : record_Chapter.id,
            "thumb_url" : record_Chapter.thumb_url,
            "title" : record_Chapter.title
        }

        chapters.append(chapter_info)

    return chapters



# 以下、サンプル


@csrf_exempt
def get_BookChapters_sample_request(request):

    '''
    ブックのチャプター一覧を取得する
    '''

    book_id = 100
    book_title = "四間飛車の定跡"
    publisher = "匿名さん"

    # bookの情報を取得する
    chapters = get_chapters_sample(book_id=book_id)

    BookChapters = {
        "book_id" : book_id,
        "book_title" : book_title,
        "publisher" : publisher,
        "chapters" : chapters
    }

    result = {
        "code" : 200,
        "result": BookChapters
    }
    
    return JsonResponse(result)


def get_chapters_sample(book_id):

    '''
    最新のブック一覧を取得する
    '''

    sample_thumb = "https://www.jma-net.go.jp/sat/data/web89/parts89/image/ir_201706201100-00.png"
    sample_thumb2 = "https://hashibaminone.com/wp-content/uploads/2018/08/LINE%E3%82%BF%E3%82%A4%E3%83%A0%E3%83%A9%E3%82%A4%E3%83%B3%E3%81%AE%E6%9C%80%E9%81%A9%E3%81%AA%E7%94%BB%E5%83%8F%E3%82%B5%E3%82%A4%E3%82%B9%E3%82%99.jpg"
    sample_thumb3 = "https://d3jks39y9qw246.cloudfront.net/medium/12036/5019cbd57e1d7b01e823a19e8ac39e8bed8a469d.jpg"


    chapters = [
        {
            "chapter_id" : 100,
            "thumb_url" : sample_thumb,
            "title" : "四間飛車の定跡",
        },
        {
            "chapter_id" : 101,
            "thumb_url" : sample_thumb3,
            "title" : "三間飛車石田流の始め方",
        },
        {
            "chapter_id" : 102,
            "thumb_url" : sample_thumb2,
            "title" : "穴熊退治の方法",
        },
    ]

    return chapters