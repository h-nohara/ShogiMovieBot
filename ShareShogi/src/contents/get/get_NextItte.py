import os, sys, json
import base64
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.user import User
from ShareShogi.models.nextItte import NextItte


parameters = [
    "title",
    "is_public",
    "favo",
    "opening_sente",
    "opening_gote",
    "choice_right",
    "choice_false_1",
    "choice_false_2",
    "message_question",
    "message_answer"
]

# id, nickname, hashtag



def get_one_NextItte(NextItte_id):

    record_NextItte = NextItte.objects.get(id=int(NextItte_id))
    info = {}

    for param in parameters:
        info[param] = record_NextItte[param]

    return info


def get_user_NextItte(user_id):

    record_User = User.objects.get(id=int(user_id))
    items = []

    for record_NextItte in NextItte.objects.filter(user=record_User):
        info = {}
        for param in parameters:
            info[param] = record_NextItte[param]
        items.append(info)

    return items


def get_user_NextItte_request(request):

    payload = request.POST
    user_id = int(payload["user_id"])
    items = get_user_NextItte(user_id)

    resp = {
        "code" : 200,
        "result" : items
    }

    return JsonResponse(resp)


@csrf_exempt
def get_NextItte_request(request):

    '''
    params = {"is_public":True, "opening_sente":None, "opening_gote":None}
    {"params" : params}
    '''

    payload = request.POST
    params = payload["params"]

    print(payload)

    items = get_NextItte(**params)

    resp = {
        "code" : 200,
        "result" : items
    }

    return JsonResponse(resp)


def get_NextItte(is_public=True, opening_sente=None, opening_gote=None):

    items = []

    if (opening_sente is None) and (opening_gote is None):
        queryset_NextItte = NextItte.objects.filter(is_public=is_public)[::-1]
    
    # あとで実装
    elif (opening_sente is not None) and (opening_gote is None):
        queryset_NextItte = NextItte.objects.filter(is_public=is_public)[::-1]
    # あとで実装
    elif (opening_sente is None) and (opening_gote is not None):
        queryset_NextItte = NextItte.objects.filter(is_public=is_public)[::-1]


    for record_NextItte in queryset_NextItte:
        info = {}
        for param in parameters:
            info[param] = record_NextItte[param]
        info["id"] = record_NextItte.id
        info["nickname"] = record_NextItte.user.nickname
        info["hashtags"] = ["三間飛車", "居飛車穴熊"]
        items.append(info)

    return items
