import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt



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
def save_NotePage_request(request):

    '''
    新たなチャプターを作成する
    '''

    # POSTを受け取る

    payload = request.POST
    print(payload)
    print(request.FILES)

    NotePage_id = int(payload["NotePage_id"])
    record_NotePage = NotePage.objects.get(id=NotePage_id)

    record_NotePage.message = payload["message"]

    # 画像をアップロード
    if payload["is_image_changed"] == "true":
        image = request.FILES["image"]
        image_url = record_NotePage.image_url
        image_url = change_image_from_post(image=image, image_url=image_url, bucket=bucket)

    record_NotePage.save()    
    print("saved new nextItte")

    return JsonResponse({"code" : 200})


def generate_temporal_path(basename):
    return os.path.abspath(os.path.join(TEMPORAL_DIR, basename))


def change_image_from_post(image, image_url, bucket):

    '''
    image : request.FILES["key"]
    image_url : fname_cloud
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

    image_basename = os.path.basename(image_url)
    assert fname_cloud(image_basename) == image_url

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
