import os, sys
import json
import random, string
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User

# api
from bot.src.line_bot_api import line_bot_api, push_text_message


@csrf_exempt
def create_new_account_request(request):
    
    create_new_account(request)

    return JsonResponse({"code" : 200})
    


def create_new_account(request):

    print("start : create new account")

    obj = json.loads(request.body.decode("utf-8"))
    data = obj["data"]

    line_id = data["line_id"]
    line_display_name = data["display_name"]
    line_thumb_path = data["picture_url"]
    line_status_message = data["status_message"]
    
    username = generate_unique_username(8)
    password = random_name(10)

    # ユーザ作成

    record_User = User(
        username = username,
        line_id = line_id,
        line_display_name = line_display_name,
        line_thumb_path = line_thumb_path
    )

    record_User.set_password(password)
    record_User.save()

    print("success : create new account")
    print("start : push username and passwd")

    push_text_message(text="ユーザ名とパスワードを送信します。大切に保管してください。", line_id=line_id)
    push_text_message(text="="*20+"\n"+"＊username\n{}\n＊password\n{}\n".format(username, password)+"="*20, line_id=line_id)

    print("finish : register new account")


def generate_unique_username(length_username):

    record_all_User = User.objects.all()
    usernames = [record_User.username for record_User in record_all_User]
    
    while True:
        name = random_name(length_username)
        if name not in usernames:
            break

    return name


def random_name(n):

    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return "".join(randlst)
