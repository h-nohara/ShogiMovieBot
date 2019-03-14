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


@csrf_exempt
def create_chapter_request(request):

    '''
    新たなチャプターを作成する
    '''

    payload = json.loads(request.body.decode("utf-8"))

    book_id = payload["book_id"]
    record_Book = Book.objects.get(id=book_id)

    # 画像のパスを生成
    thumb_fname = "hoge"
    ext = thumb_fname.split(".")[-1]
    thumb_basename = generate_basename(key=str(book_id)+"chapthumb", ext=ext)
    thumb_path = fname_cloud(thumb_basename)

    # 画像をアップロードする


    # レコードを保存
    record_Chapter = Chapter(
        book = record_Book,
        title = payload["title"],
        thumb_path = thumb_path
    )

    record_Chapter.save()
    
    return JsonResponse({"code" : 200})