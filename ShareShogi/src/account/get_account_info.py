import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from ShareShogi.models.book import Book
from ShareShogi.models.chapter import Chapter
from ShareShogi.models.scene import Scene


@csrf_exempt
def get_account_info_request(request):

    record_User = request.user

    username = record_User.username
    nickname = record_User.nickname
