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
from accounts.src.utils.aws_bucket import bucket, delete_file
from ShareShogi.src.contents.delete.delete_chapter import delete_chapter


@csrf_exempt
def delete_book_request(request):

    '''
    ブックを削除
    '''

    # book_idを取得する

    if request.method == "GET":
        if "mybook_id" in request.session:
            book_id = int(request.session["mybook_id"])
        else:
            return JsonResponse({"code" : 400})

    # elif request.method == "POST":
    #     payload = json.loads(request.body.decode("utf-8"))
    #     book_id = int(payload["book_id"])

    else:
        return JsonResponse({"code" : 400, "comment" : "only get acccept"})

    delete_book(book_id=book_id)

    result = {
        "code" : 200,
    }
    
    return JsonResponse(result)


def delete_book(book_id):

    record_Book = Book.objects.get(id=book_id)
    queryset_Chapter = Chapter.objects.filter(book=record_Book)

    # チャプター一覧を削除
    for record_Chapter in queryset_Chapter:
        delete_chapter(chapter_id=record_Chapter.id)

    # 画像を削除
    thumb_url = record_Book.thumb_url
    basename = os.path.basename(thumb_url)
    delete_file(bucket=bucket, key=basename, exist_check=True)

    print("deleted : {}".format(thumb_url))

    # レコード削除
    record_Book.delete()