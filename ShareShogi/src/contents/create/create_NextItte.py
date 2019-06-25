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
from ShareShogi.models.nextItte import NextItte

# src
from accounts.src.utils.generate_fname import generate_basename
from accounts.src.utils.aws_bucket import fname_cloud, bucket, upload_file
from accounts.src.utils.extentions import get_normalized_ext
from ShareShogi.src.FileEditor.exif_orientation import modify_by_EXIF

from ShogiMovieBot.settings import BASE_DIR  # プロジェクトディレクトリ
# 一時ファイルの保存場所
TEMPORAL_DIR = os.path.abspath(os.path.join(BASE_DIR, "ShareShogi", "temporal"))




@csrf_exempt
def create_nextItte_request(request):

    '''
    新たなチャプターを作成する
    '''

    # POSTを受け取る

    payload = request.POST
    print(payload)
    print(request.FILES)

    user_id = int(payload["user_id"])
    image_question = request.FILES["image_question"]
    image_answer = request.FILES["image_answer"]

    # 画像をアップロード
    image_url_list = []
    for i, image in enumerate([image_question, image_answer]):

        if i == 0:
            key = str(user_id) + "image_question"
        else:
            key = str(user_id) + "image_answer"

        image_url = upload_image_from_post(image=image, key=key, bucket=bucket)
        image_url_list.append(image_url)
        print("uploaded : {}".format(image_url))

    # レコードを作成

    record_User = User.objects.get(id=user_id)
    record_NextItte = NextItte(
        user = record_User,
        image_url_question = image_url_list[0],
        image_url_answer = image_url_list[1]
    )

    parameters = [
        "title",
        "is_public",
        "opening_sente",
        "opening_gote",
        "choice_right",
        "choice_false_1",
        "choice_false_2",
        "message_question",
        "message_answer"]

    for param in parameters:
        if param == "is_public":
            if payload[param] == "true":
                record_NextItte.is_public = True
            else:
                record_NextItte.is_public = False
        else:
            setattr(record_NextItte, param, payload[param])
            # record_NextItte[param] = payload[param]

    record_NextItte.save()    
    print("saved new nextItte")

    print()
    print(image_url_list)

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
