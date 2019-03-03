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
from accounts.src.project.get_projects import get_projects
from accounts.src.project.create_new_project import copy_initial_pickle_local
from accounts.src.project.create_new_project_from_history import create_new_project_from_history
from accounts.src.project.read_external_kifu.kifu_to_history import kifu_to_history
from accounts.src.project.read_external_kifu.kifu_wars2normal import kifu_wars2normal


# {"history" : [{}, {}, ...]}という形式でやり取り

@csrf_exempt
def create_new_project_from_external_kifu_request(request):

    data = json.loads(request.body.decode("utf-8"))
    kifu = data["kifu"]
    user_id = int(request.user.id)
    create_new_project_from_external_kifu(user_id=user_id, data=kifu)

    return JsonResponse({"code" : 200})


def create_new_project_from_external_kifu(user_id, data):

    '''
    data (str) : 将棋ウォーズの棋譜の文字列
    '''

    # とりあえずウォーズの棋譜のみを想定
    hands_normal, hands_str  = kifu_wars2normal(data=data)

    history = kifu_to_history(hands=hands_normal, hands_str=hands_str)
    create_new_project_from_history(user_id=user_id, history=history, title="【新規】将棋ウォーズから")