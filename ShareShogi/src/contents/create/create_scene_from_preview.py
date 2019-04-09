import os, sys, json
import base64
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import cv2
import base64
import numpy as np
import io
from PIL import Image


# db
from accounts.models.user import User
from ShareShogi.models.book import Book
from ShareShogi.models.chapter import Chapter
from ShareShogi.models.scene import Scene

# src
from accounts.src.utils.generate_fname import generate_basename
from accounts.src.utils.aws_bucket import fname_cloud, bucket, upload_file
from accounts.src.utils.extentions import get_normalized_ext

from ShogiMovieBot.settings import BASE_DIR  # プロジェクトディレクトリ
# 一時ファイルの保存場所
TEMPORAL_DIR = os.path.abspath(os.path.join(BASE_DIR, "ShareShogi", "temporal"))

def generate_temporal_path(basename):
    return os.path.abspath(os.path.join(TEMPORAL_DIR, basename))


@csrf_exempt
def create_scene_from_preview_request(request):

    '''
    新たなシーンを作成する
    '''

    # POSTを受け取る



    ######################### 1

    # payload = json.loads(request.body.decode("utf-8"))
    
    # image_payload = payload["image"]
    # text = payload["text"]

    # image_prefix, image_base64 = image_payload.split(",")
    # print(image_prefix)

    # dec_file = base64.b64decode(image_base64)

    ####################### 2

    payload = request.POST
    text = payload["text"]
    cropping_x = float(payload["cropping_x"])
    cropping_y = float(payload["cropping_y"])
    cropping_w = float(payload["cropping_w"])
    cropping_h = float(payload["cropping_h"])

    print(payload)

    image = request.FILES["original_image"]

    print(image)

    return JsonResponse({"code" : 200})

    temporal_image_path = None

    try:
        temporal_image_path = image.temporary_file_path()
        print("temporal path exists")
        print(temporal_image_path)
    except:
        print("temporal path not exist")

    #######################

    

    user_id = int(request.user.id)


    # 画像のパスを生成
    # ext = "jpg"
    # image_basename = generate_basename(key=str(user_id)+"newscene", ext=ext)
    # image_url = fname_cloud(image_basename)
    # temporal_image_path = generate_temporal_path(image_basename)

    # print(image_url)
    # print(temporal_image_path)

    ####################### 1

    # # 画像をデコードして保存
    # with open(temporal_image_path, "wb") as f:
    #     f.write(base64.b64decode(image_base64))

    # # 画像をアップロード
    # upload_file(bucket, temporal_image_path, image_basename)

    # # 画像を削除
    # os.remove(temporal_image_path)

    ######################### 2

    # 画像をアップロード

    content_type = "image/jpeg"
    ext = "jpg"

    image_basename = generate_basename(key=str(user_id)+"newscene", ext=ext)
    image_url = fname_cloud(image_basename)

    # if temporal_image_path is None:
    #     obj = bucket.Object(image_basename)
    #     response = obj.put(
    #         Body = image.read(),
    #         ContentType = content_type
    #     )
    # else:
    #     bucket.upload_file(
    #         temporal_image_path,
    #         image_basename,
    #         ExtraArgs={"ContentType": content_type}
    #     )



    # 画像をクロッピング

    if temporal_image_path is None:
        # 画像にして保存
        temporal_image_path = generate_temporal_path(image_basename)
        with open(temporal_image_path, 'wb') as f:
            f.write(image.read())
    
    im = Image.open(temporal_image_path)
    im_crop = im.crop((cropping_x, cropping_y, cropping_x+cropping_w, cropping_y+cropping_h))
    im_crop.save(temporal_image_path, quality=100)

    bucket.upload_file(
        temporal_image_path,
        image_basename,
        ExtraArgs={"ContentType": content_type}
    )

    if os.path.exists(temporal_image_path):
        os.remove(temporal_image_path)

    print("uploaded image")

    ###########################

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

        print(text_original)

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