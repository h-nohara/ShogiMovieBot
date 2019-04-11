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
def get_BookChaptersScenes_request(request):

    '''
    ブックのチャプター一覧を取得する
    '''

    # book_idを取得する

    if request.method == "GET":

        if "mybook_id" in request.session:
            book_id = int(request.session["mybook_id"])
        else:
            return JsonResponse({"code" : 400})

        if "mychapter_id" in request.session:
            chapter_id = int(request.session["mychapter_id"])
        else:
            return JsonResponse({"code" : 400})

    elif request.method == "POST":
        print("post")
        payload = json.loads(request.body.decode("utf-8"))
        book_id = int(payload["book_id"])
        chapter_id = int(payload["chapter_id"])
        print(book_id)

    # book情報を取得

    record_Book = Book.objects.get(id=book_id)

    book_title = record_Book.title
    publisher = record_Book.user.nickname

    # チャプター一覧以下の情報を取得する
    ChaptersScenes = get_ChaptersScenes(book_id=book_id)

    BookChaptersScenes = {
        "book_id" : book_id,
        "book_title" : book_title,
        "publisher" : publisher,
        "watching_chapter_id" : chapter_id,
        "ChaptersScenes" : ChaptersScenes
    }

    result = {
        "code" : 200,
        "result": BookChaptersScenes
    }
    
    return JsonResponse(result)


def get_ChaptersScenes(book_id):

    '''
    チャプター一覧以下の情報を取得する
    '''

    ChaptersScenes = []
    
    queryset_Chapter = Chapter.objects.filter(book=Book.objects.get(id=book_id))

    for record_Chapter in queryset_Chapter:

        chaper_id = record_Chapter.id

        ChapterScenes = {
            "chapter_id" : chaper_id,
            "thumb_url" : record_Chapter.thumb_url,
            "title" : record_Chapter.title,
            "scenes" : None
        }

        # シーン一覧を取得
        ChapterScenes["scenes"] = get_all_scenes(chapter_id=chaper_id)

        ChaptersScenes.append(ChapterScenes)

    return ChaptersScenes


def get_all_scenes(chapter_id):

    all_scenes = []

    queryset_Scenes = Scene.objects.filter(chapter=Chapter.objects.get(id=chapter_id))

    for record_Scene in queryset_Scenes:

        scene = {
            "scene_id" : record_Scene.id,
            "image_url" : record_Scene.image_url,
            "text" : record_Scene.text
        }

        all_scenes.append(scene)

    return all_scenes