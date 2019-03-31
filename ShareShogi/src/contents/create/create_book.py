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
from accounts.src.utils.aws_bucket import fname_cloud, bucket
from accounts.src.utils.extentions import get_normalized_ext


@csrf_exempt
def create_book_request(request):

    '''
    新たなブックを作成する
    '''

    print("create new bool request")
    print()

    payload = request.POST

    # payload = json.loads(request.body.decode("utf-8"))
    # print(payload)

    title = payload["title"]
    opening_sente = payload["opening_sente"]
    opening_gote = payload["opening_gote"]

    print(payload)
    print("")
    print("title : {}".format(title))
    print("opening_sente : {}".format(opening_sente))
    print("opening_gote : {}".format(opening_gote))
    print("")
    print(request.FILES)

    thumb = request.FILES["thumb"]
    fname = thumb._name
    content_type = thumb.content_type

    # print(thumb)
    # print(thumb.__dict__)
    print(fname)
    print(content_type)


    temporal_path = None

    try:
        temporal_path = thumb.temporary_file_path()
        print("temporal path exists")
        print(temporal_path)
    except:
        print("temporal path not exist")



    if "user_id" in payload.keys():
        user_id = int(payload["user_id"])

    else:
        user_id = int(request.user.id)

    print("user_id : {}".format(str(user_id)))


    # 画像のパスを生成
    ext_original = fname.split(".")[-1]
    ext = get_normalized_ext(ext=ext_original, restriction="image")
    assert ext is not None
    thumb_basename = generate_basename(key=str(user_id)+"bookthumb", ext=ext)
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
    record_User = User.objects.get(id=user_id)
    
    record_Book = Book(
        user = record_User,
        title = title,
        thumb_url = thumb_url,
        is_public = False,
        opening_sente = opening_sente,
        opening_gote = opening_gote
    )

    record_Book.save()

    print("saved book")

    
    # return JsonResponse({"code" : 200})

    return redirect("/ShareShogi/books/mypage")