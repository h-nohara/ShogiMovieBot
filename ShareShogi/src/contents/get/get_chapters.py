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

    '''
    ブックのチャプター一覧を取得する
    '''

    book_id = 100
    book_title = "四間飛車の定跡"
    publisher = "匿名さん"

    # bookの情報を取得する
    chapters = get_chapters(book_id=book_id)

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


def get_chapters(book_id):

    '''
    最新のブック一覧を取得する
    '''

    sample_thumb = "https://www.jma-net.go.jp/sat/data/web89/parts89/image/ir_201706201100-00.png"

    chapters = [
        {
            "chapter_id" : 100,
            "thumb_url" : sample_thumb,
            "title" : "四間飛車の定跡",
        },
        {
            "chapter_id" : 101,
            "thumb_url" : sample_thumb,
            "title" : "三間飛車石田流の始め方",
        },
        {
            "chapter_id" : 102,
            "thumb_url" : sample_thumb,
            "title" : "穴熊退治の方法",
        },
    ]

    return chapters