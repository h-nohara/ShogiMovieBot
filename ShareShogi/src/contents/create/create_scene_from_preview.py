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
    新たなシーンを作成する
    '''

    # POSTを受け取る
    payload = json.loads(request.body.decode("utf-8"))
    
    image_payload = payload["image"]
    text = payload["text"]

    image_prefix, image_base64 = image_payload.split(",")
    print(image_prefix)

    dec_file = base64.b64decode(image_base64)

    # セッション情報を取得
    user_id = int(request.user.id)
    activeSection_index = request.session["activeSection_index"]
    activeSection_id = request.session["activeSection_id"]
    activeSlide_index = request.session["activeSlide_index"]
    activeSlide_id = request.session["activeSlide_id"]
    is_create_next = request.session["is_create_next"]

    print(activeSection_index, activeSection_id, activeSlide_index, activeSlide_id, is_create_next)
    return JsonResponse({"code":200})

    # 画像のパスを生成
    ext = "jpg"
    thumb_basename = generate_basename(key=str(user_id)+"newscene", ext=ext)
    thumb_url = fname_cloud(thumb_basename)

    print(thumb_url)


    # 画像をアップロード

    obj = bucket.Object(thumb_basename)
    response = obj.put(
        Body = dec_file,
        ContentType = "image/jpeg"
    )

    print("uploaded image")

    # レコードを保存

    record_Book = Book.objects.get(id=book_id)
    
    record_Chapter = Chapter(
        book = record_Book,
        title = title,
        thumb_url = thumb_url,
    )

    record_Chapter.save()

    print("saved chapter")

    return redirect("/ShareShogi/chapters/mypage")