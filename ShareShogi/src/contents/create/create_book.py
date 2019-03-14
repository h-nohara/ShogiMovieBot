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
from accounts.src.utils.generate_fname import generate_basename
from accounts.src.utils.aws_bucket import fname_cloud
from accounts.src.utils.extentions import get_normalized_ext


@csrf_exempt
def create_book_request(request):

    '''
    新たなブックを作成する
    '''

    print("create new bool request")
    print()
    payload = request.POST
    print(payload)
    print()
    print("title : {}".format(payload["title"]))
    print("name : {}".format(payload["thumb"]))
    print(type(payload["thumb"]))

    # payload = json.loads(request.body.decode("utf-8"))
    # print(payload)

    print(request.FILES)

    return JsonResponse({"code" : 200})

    if "user_id" in payload.keys():
        user_id = int(payload["user_id"])

    else:
        user_id = int(request.user.id)

    # 画像のパスを生成
    thumb_fname = "hoge"
    ext_original = thumb_fname.split(".")[-1]
    ext = get_normalized_ext(ext=ext_original, restriction="image")
    assert ext is not None
    thumb_basename = generate_basename(key=str(user_id)+"bookthumb", ext=ext)
    thumb_path = fname_cloud(thumb_basename)

    # 画像をアップロード

    # レコードを保存
    record_User = User.objects.get(id=user_id)
    
    record_Book = Book(
        user = record_User,
        title = payload["title"],
        thumb_path = thumb_path,
        is_public = False,
        senkei_sente = payload["senkei_sente"],
        senkei_gote = payload["senkei_gote"]
    )

    record_Book.save()

    
    return JsonResponse({"code" : 200})