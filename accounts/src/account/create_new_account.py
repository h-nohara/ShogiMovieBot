import os, sys
import json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User


@csrf_exempt
def create_new_account(request):

    if not request.user.is_superuser:
        raise("not super user")

    data = json.loads(request.body.decode("utf-8"))
    username = data["username"]
    password = data["password"]
    print(username)
    print(password)

    # 同じ名前のユーザがいないかチェック
    record_list_User = User.objects.filter(username=username)
    if len(record_list_User) > 0:
        return JsonResponse({"code" : 400, "error_message" : "その名前はすでに使われています"})


    # ユーザ作成

    record_User = User(
        username = username,
        is_superuser = False,
    )
    record_User.set_password(password)

    record_User.save()
    user_id = record_User.id

    print("success : make new account")
    
    return JsonResponse({"code" : 200, "result" : {"user_id" : user_id}})
