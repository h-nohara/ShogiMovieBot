import os, sys, json
import base64
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# import cv2
# import base64
# import numpy as np
# import io
# from PIL import Image


# db
from accounts.models.user import User
from ShareShogi.models.note import Note
from ShareShogi.models.note_page import NotePage

# src
from accounts.src.utils.generate_fname import generate_basename
from accounts.src.utils.aws_bucket import fname_cloud, bucket, upload_file
from accounts.src.utils.extentions import get_normalized_ext
from ShareShogi.src.FileEditor.exif_orientation import modify_by_EXIF

from ShogiMovieBot.settings import BASE_DIR  # プロジェクトディレクトリ
# 一時ファイルの保存場所
TEMPORAL_DIR = os.path.abspath(os.path.join(BASE_DIR, "ShareShogi", "temporal"))




@csrf_exempt
def create_Note_request(request):

    '''
    新たなノートを作成する
    '''

    # POSTを受け取る

    payload = request.POST
    print(payload)
    print(request.FILES)

    user_id = int(payload["user_id"])
    image = request.FILES["image"]

    # 画像をアップロード
    key = str(user_id) + "image"
    image_url = upload_image_from_post(image=image, key=key, bucket=bucket)
    print("uploaded : {}".format(image_url))

    # ノートレコードを作成

    if payload["is_public"] == "true":
        is_public = True
    else:
        is_public = False

    record_User = User.objects.get(id=user_id)
    record_Note = Note(
        user = record_User,
        thumb_url = image_url,
        title = payload["title"],
        opening_sente = payload["opening_sente"],
        opening_gote = payload["opening_gote"],
        is_public = is_public
    )

    record_Note.save()    
    print("saved new note")


    # ノートページを作成
    record_NotePage = NotePage(
        note = record_Note,
        image_url = image_url,
        message = payload["title"],
        order_in_parent = 0
    )
    record_NotePage.save()

    return JsonResponse({"code" : 200})


@csrf_exempt
def add_NotePage_request(request):

    payload = request.POST
    print(payload)
    print(request.FILES)

    note_id = int(payload["note_id"])
    order = int(payload["order"])
    message = payload["message"]
    image = request.FILES["image"]

    # 画像をアップロード
    key = str(note_id) + "newNotePage"
    image_url = upload_image_from_post(image=image, key=key, bucket=bucket)
    print("uploaded : {}".format(image_url))

    record_Note = Note.objects.get(id=note_id)

    # 表紙ページの変更だった場合、ノート情報を更新
    if order == 0:
        record_Note.title = message
        record_Note.thumb_url = image_url
        record_Note.save()

    queryset_NotePage = NotePage.objects.filter(note=record_Note)

    # インデックスを更新
    for record_NotePage in queryset_NotePage[order:]:
        record_NotePage.order_in_parent = record_NotePage.order_in_parent + 1
        record_NotePage.save()

    # ノートページを作成
    record_NotePage = NotePage(
        note = record_Note,
        image_url = image_url,
        message = message,
        order_in_parent = order
    )
    record_NotePage.save()

    return JsonResponse({"code" : 200})



def generate_temporal_path(basename):
    return os.path.abspath(os.path.join(TEMPORAL_DIR, basename))


def upload_image_from_post(image, key, bucket):

    '''
    image : request.FILES["key"]
    key : unique name
    '''

    content_type = image.content_type

    if content_type not in ["image/jpeg", "image/png"]:
        content_type = "image/jpeg"

    if content_type == "image/png":
        ext = "png"
    else:
        ext = "jpg"

    temporal_image_path = None
    try:
        temporal_image_path = image.temporary_file_path()
        print("temporal path exists")
        print(temporal_image_path)
    except:
        print("temporal path not exist")

    image_basename = generate_basename(key=key, ext=ext)
    image_url = fname_cloud(image_basename)

    # もしオンメモリデータだったら、画像にして保存
    if temporal_image_path is None:
        temporal_image_path = generate_temporal_path(image_basename)
        with open(temporal_image_path, 'wb') as f:
            f.write(image.read())

    # アップロード
    bucket.upload_file(
        temporal_image_path,
        image_basename,
        ExtraArgs={"ContentType": content_type}
    )

    if os.path.exists(temporal_image_path):
        os.remove(temporal_image_path)

    return image_url 
