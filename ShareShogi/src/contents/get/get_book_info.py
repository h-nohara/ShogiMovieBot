import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from ShareShogi.models.book import Book
from ShareShogi.models.chapter import Chapter
from ShareShogi.models.scene import Scene


@csrf_exempt
def get_book_info_request(request):

    '''
    特定のブックと、それに属するチャプター・シーンに関する情報を取得する
    '''

    payload = json.loads(request.body.decode("utf-8"))
    book_id = int(payload["id"])

    book_info = get_book_info(book_id, get_childs=True)

    result = {
        "code" : 200,
        "result": book_info
    }

    
    return JsonResponse(result)


def get_book_info(book_id, get_childs=False):

    '''
    特定のブックに関する情報を取得する
    
    get_childs : Trueなら、ブックに属する全てのチャプター情報も加える
    '''

    record_Book = Book.objects.get(id=book_id)

    book_info = {
        "nickname" : record_Book.user.nickname,
        "title" : record_Book.title,
        "thumb_url" : record_Book.thumb_path,
        "is_public" : record_Book.is_public,
        "senkei_sente" : record_Book.senkei_sente,
        "senkei_gote" : record_Book.senkei_gote,
    }

    # チャプター情報を加える
    if get_childs:
        chapters = get_all_chapters(book_id, get_childs=True)
        book_info["chapters"] = chapters

    return book_info


def get_all_chapters(book_id, get_childs=False):

    '''
    特定のチャプターに関する情報を取得する
    
    get_childs : Trueなら、チャプターに属する全てのシーン情報も加える
    '''

    record_Book = Book.objects.get(id=book_id)
    queryset_Chapter = Chapter.objects.filter(book=record_Book)

    chapters = []

    for record_Chapter in queryset_Chapter:

        chapter_id = int(record_Chapter.id)

        chapter_info = {
            "id" : chapter_id,
            "title" : record_Chapter.title,
            "thumb_url" : record_Chapter.thumb_path,
        }

        # 全てのシーン情報を加える
        if get_childs:
            scenes = get_all_scenes(chapter_id)
            chapter_info["scenes"] = scenes

        chapters.append(chapter_info)

    return chapters


def get_all_scenes(chapter_id):

    record_Chapter = Chapter.objects.get(chapter_id)
    queryset_Scene = Scene.objects.filter(chapter=record_Chapter)

    scenes = []

    for record_Scene in queryset_Scene:

        scene_info = {
            "id" : int(record_Scene.id),
            "text" : record_Scene.text,
            "image_path" : record_Scene.image_path,
            "movie_path" : record_Scene.movie_path
        }

        scenes.append(scene_info)

    return scenes