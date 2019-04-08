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

    payload = request.POST

    print(payload)
    print()
    print(request.FILES)
    print()
    # print(request.form)
    print()

    print("================")
    print()

    payload = json.loads(request.body.decode("utf-8"))
    # print(payload)
    # print()
    image_enc = payload["image"]
    text = payload["text"]

    split_imageobj = image_enc.split(",")
    print(len(split_imageobj))
    print(split_imageobj[0])
    print(split_imageobj[1][:100])

    dec_file = base64.b64decode(split_imageobj[1])

    basename = "hohohoho.jpg"
    print(fname_cloud(basename))
    obj = bucket.Object(basename)
    response = obj.put(
        Body = obj,
        ContentType = "image/jpeg"
    )

    # def convert_b64_string_to_file(s, outfile_path):
    #     """base64をデコードしてファイルに書き込む"""
    #     with open(outfile_path, "wb") as f:
    #         f.write(base64.b64decode(s))

    # text = payload["text"]
    # image = request.FILES["image"]
    # fname = image._name
    # content_type = image.content_type

    # print(thumb)
    # print(thumb.__dict__)
    # print(fname)
    # print(content_type)

    return JsonResponse({"code" : 200})

    activeSection_index = request.session["activeSection_index"]
    activeSection_id = request.session["activeSection_id"]
    activeSlide_index = request.session["activeSlide_index"]
    activeSlide_id = request.session["activeSlide_id"]
    is_create_next = request.session["is_create_next"]


    temporal_path = None

    try:
        temporal_path = thumb.temporary_file_path()
        print("temporal path exists")
        print(temporal_path)
    except:
        print("temporal path not exist")


    # 画像のパスを生成
    ext_original = fname.split(".")[-1]
    ext = get_normalized_ext(ext=ext_original, restriction="image")
    assert ext is not None
    thumb_basename = generate_basename(key=str(user_id)+"chapterthumb", ext=ext)
    thumb_url = fname_cloud(thumb_basename)

    print(thumb_url)


    # 画像をアップロード

    if temporal_path is None:
        obj = bucket.Object(thumb_basename)
        response = obj.put(
            Body = thumb.read(),
            ContentType = content_type
        )
    else:
        bucket.upload_file(
            temporal_path,
            thumb_basename,
            ExtraArgs={"ContentType": content_type}
        )

    print("uploaded thumb image")

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