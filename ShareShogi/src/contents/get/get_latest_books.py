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

    queryset_Book = Book.objects.filter(is_public=True)
    books = []

    for record_Book in queryset_Book:

        info = {
            "book_id" : int(record_Book.id),
            "thumb_url" : record_Book.thumb_url,
            "title" : record_Book.title,
            "publisher" : record_Book.user.nickname,
            "opening" : {
                "sente" : record_Book.opening_sente,
                "gote" : record_Book.opening_gote
            }
        }
        books.append(info)

    books = books[::-1]

    return books


def get_latest_books_sample():

    '''
    最新のブック一覧を取得する
    '''

    sample_thumb = "https://www.jma-net.go.jp/sat/data/web89/parts89/image/ir_201706201100-00.png"
    sample_thumb2 = "https://hashibaminone.com/wp-content/uploads/2018/08/LINE%E3%82%BF%E3%82%A4%E3%83%A0%E3%83%A9%E3%82%A4%E3%83%B3%E3%81%AE%E6%9C%80%E9%81%A9%E3%81%AA%E7%94%BB%E5%83%8F%E3%82%B5%E3%82%A4%E3%82%B9%E3%82%99.jpg"
    sample_thumb3 = "https://d3jks39y9qw246.cloudfront.net/medium/12036/5019cbd57e1d7b01e823a19e8ac39e8bed8a469d.jpg"

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
        {
            "book_id" : 103,
            "thumb_url" : sample_thumb2,
            "title" : "三間飛車石田流の始め方",
            "publisher" : "匿名さん",
            "opening" : {"sente" : "SikenBisha", "gote" : "SankenBisha"}
        },
        {
            "book_id" : 104,
            "thumb_url" : sample_thumb3,
            "title" : "穴熊退治の方法",
            "publisher" : "匿名さん",
            "opening" : {"sente" : "SikenBisha", "gote" : "SankenBisha"}
        },
    ]

    return books