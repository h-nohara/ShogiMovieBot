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
from accounts.src.utils.aws_bucket import bucket, delete_file
from ShareShogi.src.contents.delete.delete.scene import delete_scene


@csrf_exempt
def delete_chapter_request(request):

    '''
    チャプターを削除
    '''

    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))

    else:
        raise("only POST accept")

    chapter_id = int(payload["chapter_id"])
    delete_chapter(chapter_id=chapter_id)

    result = {
        "code" : 200,
    }
    
    return JsonResponse(result)


def delete_chapter(chapter_id):

    record_Chapter = Chapter.objects.get(id=chapter_id)
    queryset_Scene = Scene.objects.filter(chapter=record_Chapter)

    # 全シーンを削除
    for record_Scene in queryset_Scene:
        delete_scene(scene_id=record_Scene.id)

    # 画像を削除
    thumb_url = record_Chapter.thumb_url
    basename = os.path.basename(thumb_url)
    delete_file(bucket=bucket, key=basename, exist_check=True)

    print("deleted : {}".format(thumb_url))

    # レコード削除
    record_Chapter.delete()