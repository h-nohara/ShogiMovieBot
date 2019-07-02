import os, sys, json
import base64
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.user import User
from ShareShogi.models.note import Note
from ShareShogi.models.note_page import NotePage



# １つのノートの情報を取得

@csrf_exempt
def get_NoteInfo_request(request):

    payload = json.loads(request.body.decode("utf-8"))
    # payload = request.POST
    note_id = int(payload["note_id"])
    info = get_NoteInfo(note_id)

    return JsonResponse({"code" : 200, "result" : info})


def get_NoteInfo(note_id):

    record_Note = Note.objects.get(id=note_id)
    info = {
        "nickname" : record_Note.user.nickname,
        "id" : record_Note.id,
        "opening_sente" : record_Note.opening_sente,
        "opening_gote" : record_Note.opening_gote,
        "is_public" : record_Note.is_public,
        "pages" : [],
        "hashtags" : ["三間飛車", "居飛車穴熊"]
    }


    for record_NotePage in record_NotePage.objects.filter(note=record_Note):
        info["pages"].append(
            {
                "image_url" : record_NotePage.image_url,
                "message" : record_NotePage.message
            }
        )

    return info



# ユーザーのノート一覧を取得

def get_user_Note_request(request):

    payload = json.loads(request.body.decode("utf-8"))
    user_id = int(payload["user_id"])
    notes = get_user_Note(user_id)

    return JsonResponse({"code" : 200, "result" : notes})


def get_user_Note(user_id):

    record_User = User.objects.get(id=int(user_id))
    items = []

    for record_Note in Note.objects.filter(user=record_User)[::-1]:

        info = {
            "id" : record_Note.id,
            "title" : record_Note.title,
            "thumb" : record_Note.thumb_url,
            "opening_sente" : record_Note.opening_sente,
            "opening_gote" : record_Note.opening_gote,
            "is_public" : record_Note.is_public,

            "hashtags" : ["三間飛車", "居飛車穴熊"]
        }
        items.append(info)

    return items



# ノート一覧の検索結果を取得


@csrf_exempt
def get_Note_request(request):

    '''
    params = {"is_public":True, "opening_sente":None, "opening_gote":None}
    {"params" : params}
    '''

    print("")
    print("====")

    # payload = request.POST
    payload = json.loads(request.body.decode("utf-8"))
    print(payload)
    params = payload["params"]

    items = get_Note(**params)

    resp = {
        "code" : 200,
        "result" : items
    }

    return JsonResponse(resp)


def get_Note(is_public=True, opening_sente=None, opening_gote=None):

    items = []
    
    # あとで実装
    if (opening_sente is not None) and (opening_gote is None):
        queryset_Note = Note.objects.filter(is_public=is_public)
    # あとで実装
    elif (opening_sente is None) and (opening_gote is not None):
        queryset_Note = Note.objects.filter(is_public=is_public)

    else:
        queryset_Note = Note.objects.filter(is_public=is_public)


    for record_Note in queryset_Note[::-1]:

        info = {
            "id" : record_Note.id,
            "title" : record_Note.title,
            "thumb" : record_Note.thumb_url,
            "opening_sente" : record_Note.opening_sente,
            "opening_gote" : record_Note.opening_gote,
            "is_public" : record_Note.is_public,
            "favo" : record_Note.favo,

            "nickname" : record_Note.user.nickname,
            "hashtags" : ["三間飛車", "居飛車穴熊"]
        }
        items.append(info)

    return items
