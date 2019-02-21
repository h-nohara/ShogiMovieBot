#!/user/bin/env python 
# -*- coding: utf-8 -*-

import os, sys, glob2, shutil, copy, pickle
import json


from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project

# api
from accounts.src.utils import pickle_path_local, generate_pickle_path_local
from accounts.src.utils.generate_fname import INITIAL_PICKLE, generate_basename
from accounts.src.utils.aws_bucket import fname_cloud
from .modify import modify
from accounts.src.project.get_projects import get_projects
from accounts.src.project.create_new_project import copy_initial_pickle_local


# {"history" : [{}, {}, ...]}という形式でやり取り

@csrf_exempt
def save_initial_board_request(request):

    data = json.loads(request.body.decode("utf-8"))
    title = data["title"]
    history = data["history"]

    # プロジェクトを新規作成
    user_id = int(request.user.id)
    record_User = User.objects.get(id=user_id)
    username = record_User.username
    the_key = username + str(title)
    path_local, pickle_basename = generate_pickle_path_local(key=the_key, get_basename=True)

    # pickleをコピー
    copy_initial_pickle_local(path_local)

    # concat_movie_pathを「生成
    concat_movie_basename = generate_basename(key=the_key+"concatmoviebasename", ext="mp4")

    # プロジェクトを保存
    record_Project = Project(
        user = record_User,
        title = title,
        pickle_basename = pickle_basename,
        concat_movie_path = fname_cloud(concat_movie_basename)
    )

    record_Project.save()

    # 盤面を保存

    # なぜかmoveの「＋」が抜けてしまうので、対策
    history = modify(history)

    result = {"history" : history}

    with open(path_local, mode="wb") as f:
        pickle.dump(result, f)

    print("success : save_pickle")

    return JsonResponse({"code" : 200})