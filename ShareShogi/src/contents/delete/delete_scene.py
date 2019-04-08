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


@csrf_exempt
def delete_scene_request(request):

    '''
    シーンを削除
    '''

    if request.method == "GET":
        raise("only POST accept")

    elif request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))

    scene_id = int(payload["scene_id"])
    delete_scene(scene_id=scene_id)

    result = {
        "code" : 200,
    }
    
    return JsonResponse(result)


def delete_scene(scene_id):

    record_Scene = Scene.objects.get(id=scene_id)

    image_url = record_Scene.image_url
    basename = os.path.basename(image_url)

    delete_file(bucket=bucket, key=basename, exist_check=True)