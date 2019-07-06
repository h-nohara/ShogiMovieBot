import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt



# db
from accounts.models.user import User
from ShareShogi.models.note import Note

# src
from accounts.src.utils.generate_fname import generate_basename
from accounts.src.utils.aws_bucket import fname_cloud, bucket, upload_file
from accounts.src.utils.extentions import get_normalized_ext
from ShareShogi.src.FileEditor.exif_orientation import modify_by_EXIF

from ShogiMovieBot.settings import BASE_DIR  # プロジェクトディレクトリ
# 一時ファイルの保存場所
TEMPORAL_DIR = os.path.abspath(os.path.join(BASE_DIR, "ShareShogi", "temporal"))




@csrf_exempt
def save_Note_settings_request(request):

    '''
    新たなチャプターを作成する
    '''

    # POSTを受け取る

    payload = json.loads(request.body.decode("utf-8"))
    print(payload)

    note_id = int(payload["note_id"])
    record_Note = Note.objects.get(id=note_id)

    # 公開設定
    if payload["is_public"] == "true":
        record_Note.is_public = True
    else:
        record_Note.is_public = False

    # 戦型
    record_Note.opening_sente = payload["opening_sente"]
    record_Note.opening_gote = payload["opening_gote"]

    record_Note.save()    
    print("saved note settings")

    return JsonResponse({"code" : 200})

