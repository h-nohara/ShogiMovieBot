import os, sys, json
import base64
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from ShareShogi.models.book import Book
from ShareShogi.models.chapter import Chapter
from ShareShogi.models.scene import Scene

# src
from accounts.src.utils.generate_fname import generate_basename
from accounts.src.utils.aws_bucket import fname_cloud, bucket
from accounts.src.utils.extentions import get_normalized_ext


@csrf_exempt
def create_scene_from_preview_request(request):

    '''
    新たなチャプターを作成する
    '''

    # POSTを受け取る
    payload = json.loads(request.body.decode("utf-8"))
    
    image_payload = payload["image"]
    text = payload["text"]

    image_prefix, image_base64 = image_payload.split(",")
    print(image_prefix)

    dec_file = base64.b64decode(image_base64)

    user_id = int(request.user.id)


    # 画像のパスを生成
    ext = "jpg"
    image_basename = generate_basename(key=str(user_id)+"newscene", ext=ext)
    image_url = fname_cloud(image_basename)

    print(image_url)


    # 画像をアップロード

    obj = bucket.Object(image_basename)
    response = obj.put(
        Body = dec_file,
        ContentType = "image/jpeg"
    )

    print("uploaded image")

    # セッション情報を取得
    activeSection_index = request.session["activeSection_index"]
    activeSection_id = request.session["activeSection_id"]
    activeSlide_index = request.session["activeSlide_index"]
    activeSlide_id = request.session["activeSlide_id"]
    is_create_next = request.session["is_create_next"]

    insert_scene(
        chapter_id = activeSection_id,
        index = activeSlide_index-1,
        is_create_next = is_create_next,
        new_scene_info = {
            "text" : text,
            "image_url" : image_url
        }
    )

    return JsonResponse({"code" : 200})


def insert_scene(chapter_id, index, is_create_next, new_scene_info):

    '''
    index : 挿入する
    '''

    # チャプターにシーンを挿入

    record_Chapter = Chapter.objects.get(id=chapter_id)
    queryset_Scene = Scene.objects.filter(chapter=record_Chapter)
    n_scene = len(queryset_Scene)

    # 新規シーンが一番後ろなら
    if (n_scene == 0) or (is_create_next and (n_scene==index+1)):

        new_record_Scene = Scene(
            chapter = record_Chapter,
            text = new_scene_info["text"],
            image_url = new_scene_info["image_url"]
        )
        new_record_Scene.save()

        return

    # そうでなかったら

    if is_create_next:
        queryset_Scene = Scene.objects.filter(chapter=record_Chapter)[index+1:]
    else:
        queryset_Scene = Scene.objects.filter(chapter=record_Chapter)[index:]

    next_scene_text = None
    next_scene_image_url = None

    for record_Scene in queryset_Scene:

        text_original = record_Scene.text
        image_url_original = record_Scene.image_url

        # 元あるレコードを更新

        if next_scene_text is None:
            record_Scene.text = new_scene_info["text"]
            record_Scene.image_url = new_scene_info["image_url"]

        else:
            record_Scene.text = next_scene_text,
            record_Scene.image_url = next_scene_image_url

        record_Scene.save()

        # 元のレコード情報を次に渡す
        next_scene_text = text_original
        next_scene_image_url = image_url_original

    assert next_scene_text is not None

    new_record_Scene = Scene(
        chapter = record_Chapter,
        text = next_scene_text,
        image_url = next_scene_image_url
    )
    new_record_Scene.save()

    return