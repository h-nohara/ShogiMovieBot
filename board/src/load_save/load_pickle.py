#!/user/bin/env python 
# -*- coding: utf-8 -*-

import os, sys, glob2, subprocess, shutil, copy, pickle
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import re
import json

# from src_python.make_movie.history_to_movie import history_to_movies



import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project

# api
from accounts.src.utils import pickle_path_local



# {"history" : [{}, {}, ...]}という形式でやり取り


@csrf_exempt
def load_pickle(request):

    if request.method == "GET":
        project_id = request.session.get("project_id")
    else:
        data = json.loads(request.body.decode("utf-8"))
        project_id = data["project_id"]
    
    project_id = int(project_id)

    record_Project = Project.objects.get(id=project_id)
    project_title = record_Project.title
    pickle_basename = record_Project.pickle_basename

    pickle_path = pickle_path_local(pickle_basename)

    with open(pickle_path, mode="rb") as f:
        result = pickle.load(f)
        history = result["history"]

    json_response = {
        "code" : 200,
        "result" : {
            "history" : history,
            "project_title" : project_title
        }
    }

    print("success : load pickle : project_id={}".format(str(project_id)))

    return JsonResponse(json_response)



############################################################



# def save(request):

#     # なぜかmoveの「＋」が抜けてしまうので、対策
#     history = modify(history)

#     result = {"history" : history}
#     global PICKLE_DIR
#     fname = os.path.join(PICKLE_DIR, without_ext + ".pickle")
#     with open(fname, mode="wb") as f:
#         pickle.dump(result, f)



# # save
# @app.route("/save/<without_ext>", methods=["POST"])
# def save_history(without_ext):

#     print("="*10)
#     history = decode_to_dict(request)["history"]

#     # なぜかmoveの「＋」が抜けてしまうので、対策
#     history = modify(history)

#     result = {"history" : history}
#     global PICKLE_DIR
#     fname = os.path.join(PICKLE_DIR, without_ext + ".pickle")
#     with open(fname, mode="wb") as f:
#         pickle.dump(result, f)

#     return "hoge"


# # load
# @app.route("/load/<without_ext>")
# def load_history(without_ext):

#     global PICKLE_DIR
#     fname = os.path.join(PICKLE_DIR, without_ext + ".pickle")
#     with open(fname, mode="rb") as f:
#         result = pickle.load(f)
#     history = result["history"]

#     return jsonify({"history" : history})


# # HistoryをJSから受け取り、それを元に画像を生成する
# @app.route("/make_movie", methods=["POST"])
# def make_movie():

#     print("start make movie")
#     history = decode_to_dict(request)["history"]
#     history = modify(history)
                
#     global TEMPORAL_IMAGE_DIR
#     global RESULT_MOVIE_DIR

#     if os.path.exists(TEMPORAL_IMAGE_DIR):
#         shutil.rmtree(TEMPORAL_IMAGE_DIR)
#     os.makedirs(TEMPORAL_IMAGE_DIR)

#     if not os.path.exists(RESULT_MOVIE_DIR):
#         os.makedirs(RESULT_MOVIE_DIR)

#     history_to_movies(history, TEMPORAL_IMAGE_DIR, RESULT_MOVIE_DIR)

#     return "hoge"