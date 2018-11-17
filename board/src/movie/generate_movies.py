import os, sys, json, shutil, pickle
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project
from board.models.movie import Movie


# api
from board.src.load_save.modify import modify
from board.src.generate_movie.make_movie.history_to_movie import history_to_movies
from accounts.src.utils import generate_basename, movie_path_local, pickle_path_local


@csrf_exempt
def generate_movies(request):

    print("start : generate movie")

    data = json.loads(request.body.decode("utf-8"))
    project_id = data["project_id"]
    project_id = int(project_id)

    record_Project = Project.objects.get(id=project_id)
    pickle_basename = record_Project.pickle_basename
    key = pickle_basename.split(".")[0]

    # pickleから読み込み
    pickle_path = pickle_path_local(pickle_basename)
    with open(pickle_path, mode="rb") as f:
        result = pickle.load(f)
        history = result["history"]

    # image dir
    temporal_image_dir = movie_path_local("temporal_image_"+key)  # dir name
    if os.path.exists(temporal_image_dir):
        shutil.rmtree(temporal_image_dir)
    os.makedirs(temporal_image_dir)
    print("temporal_image_dir : {}".format(temporal_image_dir))

    # movie dir
    temporal_movie_dir = movie_path_local("temporal_movie_"+key)  # dir name
    if os.path.exists(temporal_movie_dir):
        shutil.rmtree(temporal_movie_dir)
    os.makedirs(temporal_movie_dir)
    print("temporal_movie_dir : {}".format(temporal_movie_dir))

    # 動画生成
    history_to_movies(history, temporal_image_dir, temporal_movie_dir)

    print("success : generate movies")

    # todo
    # 動画のpathを決め、Movieレコードとして保存
    # クラウドのストレージの登録
    # 動画のアップロード

    return JsonResponse({"code" : 200})