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
from ShareShogi.src.contents.get.get_book_info import get_book_info


@csrf_exempt
def get_latest_books_request(request):

    '''
    最新のブック一覧を取得する
    '''

    # bookの情報を取得する
    books = get_latest_books()

    result = {
        "code" : 200,
        "result": books
    }
    
    return JsonResponse(result)


def get_latest_books():

    '''
    最新のブック一覧を取得する
    '''

    sample_thumb = "https://www.jma-net.go.jp/sat/data/web89/parts89/image/ir_201706201100-00.png"

    books = [
        {
            "book_id" : 100,
            "thumb_url" : sample_thumb,
            "title" : "四間飛車の定跡",
            "publisher" : "匿名さん",
            "opening" : {"sente" : "SikenBisha", "gote" : "SankenBisha"}
        },
        {
            "book_id" : 101,
            "thumb_url" : sample_thumb,
            "title" : "三間飛車石田流の始め方",
            "publisher" : "匿名さん",
            "opening" : {"sente" : "SikenBisha", "gote" : "SankenBisha"}
        },
        {
            "book_id" : 102,
            "thumb_url" : sample_thumb,
            "title" : "穴熊退治の方法",
            "publisher" : "匿名さん",
            "opening" : {"sente" : "SikenBisha", "gote" : "SankenBisha"}
        },
    ]

    return books