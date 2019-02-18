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
from .modify import modify



# {"history" : [{}, {}, ...]}という形式でやり取り

@csrf_exempt
def save_pickle(request):

    data = json.loads(request.body.decode("utf-8"))
    history = data["history"]

    project_id = int(request.session.get("project_id"))

    record_Project = Project.objects.get(id=project_id)
    basename = record_Project.pickle_basename

    # なぜかmoveの「＋」が抜けてしまうので、対策
    history = modify(history)

    result = {"history" : history}

    fname = pickle_path_local(basename)
    with open(fname, mode="wb") as f:
        pickle.dump(result, f)

    print("success : save_pickle")

    return JsonResponse({"code" : 200})