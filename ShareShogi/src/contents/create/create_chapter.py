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
from ShareShogi.src.FileEditor.exif_orientation import modify_by_EXIF

from ShogiMovieBot.settings import BASE_DIR  # プロジェクトディレクトリ
# 一時ファイルの保存場所
TEMPORAL_DIR = os.path.abspath(os.path.join(BASE_DIR, "ShareShogi", "temporal"))

def generate_temporal_path(basename):
    return os.path.abspath(os.path.join(TEMPORAL_DIR, basename))


@csrf_exempt
def create_chapter_request(request):

    '''
    新たなチャプターを作成する
    '''

    # POSTを受け取る

    payload = request.POST
    text = payload["text"]
    cropping_x = float(payload["cropping_x"])
    cropping_y = float(payload["cropping_y"])
    cropping_w = float(payload["cropping_w"])
    cropping_h = float(payload["cropping_h"])

    print(payload)

    image = request.FILES["original_image"]
    content_type = image.content_type

    # セッション情報の取得
    if "user_id" in payload.keys():
        user_id = int(payload["user_id"])
    else:
        user_id = int(request.user.id)

    # book_idを取得
    if "mybook_id" in request.session:
        book_id = int(request.session["mybook_id"])
    else:
        return JsonResponse({"code" : 400, "comment" : "mybook_idが見つかりません"})

    # 画像の保存先を決める

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

    image_basename = generate_basename(key=str(user_id)+"newchapter", ext=ext)
    image_url = fname_cloud(image_basename)

    # 画像を読み込み

    if temporal_image_path is None:
        # もしオンメモリデータだったら、画像にして保存
        temporal_image_path = generate_temporal_path(image_basename)
        with open(temporal_image_path, 'wb') as f:
            f.write(image.read())
    
    im = Image.open(temporal_image_path)

    # exifに基づいて修正
    im_modify = modify_by_EXIF(im)
    if im_modify is not None:
        im = im_modify

    im_crop = im.crop((cropping_x, cropping_y, cropping_x+cropping_w, cropping_y+cropping_h))

    # スマホから送信すると"**.upload"という拡張子になることがあるので対策
    if get_normalized_ext(temporal_image_path.split(".")[-1], restriction="image") is None:
        temporal_image_path = ".".join(temporal_image_path.split(".")[:-1] + [ext])

    # 画像をトリミング
    if ext == "jpg":
        im_crop.save(temporal_image_path, quality=100)
    else:
        im_crop.save(temporal_image_path)

    # アップロード
    bucket.upload_file(
        temporal_image_path,
        image_basename,
        ExtraArgs={"ContentType": content_type}
    )

    if os.path.exists(temporal_image_path):
        os.remove(temporal_image_path)

    print("uploaded image")


    # レコードを保存

    record_Book = Book.objects.get(id=book_id)
    
    record_Chapter = Chapter(
        book = record_Book,
        title = text,
        thumb_url = image_url,
    )

    record_Chapter.save()

    print("saved chapter")

    return JsonResponse({"code" : 200})