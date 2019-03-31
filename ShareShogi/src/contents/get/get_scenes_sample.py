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
def get_BookChaptersScenes_sample_request(request):

    '''
    ブックのチャプター一覧を取得する
    '''

    book_id = 100
    book_title = "四間飛車の定跡"
    publisher = "匿名さん"

    # bookの情報を取得する
    ChaptersScenes = get_ChaptersScenes_sample(book_id=book_id)

    BookChaptersScenes = {
        "book_id" : book_id,
        "book_title" : book_title,
        "publisher" : publisher,
        "ChaptersScenes" : ChaptersScenes
    }

    result = {
        "code" : 200,
        "result": BookChaptersScenes
    }
    
    return JsonResponse(result)


def get_ChaptersScenes_sample(book_id):

    '''
    
    '''

    ChaptersScenes = []

    for i in range(3):

        ChaptersScenes.append(get_ChapterScenes_sample(chapter_id=i))

    return ChaptersScenes


def get_ChapterScenes_sample(chapter_id):

    sample_thumb = "https://www.jma-net.go.jp/sat/data/web89/parts89/image/ir_201706201100-00.png"
    
    ChapterScenes = {
        "chapter_id" : chapter_id,
        "thumb_url" : sample_thumb,
        "title" : "四間飛車の定跡",
        "scenes" : []
    }

    for i in range(4):

        scene = {
            "scene_id" : i,
            "thumb_url" : sample_thumb,
            "text" : "この局面で、歩を取ると圧倒的に不利になってしまいます",
        }

        ChapterScenes["scenes"].append(scene)

    return ChapterScenes