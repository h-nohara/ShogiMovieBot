import os, sys, json
import shutil
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project
from board.models.movie import Movie
from bot.models.scenario import Scenario

# api
from accounts.src.utils import pickle_path_local
from accounts.src.utils.aws_bucket import bucket, delete_file
from board.src.movie.get_movies import get_movies
from bot.src.delete_scenario import delete_scenario


@csrf_exempt
def delete_project_request(request):

    payload = json.loads(request.body.decode("utf-8"))
    project_id = payload["project_id"]
    project_id = int(project_id)

    delete_project(project_id)

    return JsonResponse({"code" : 200})


def delete_project(project_id):

    record_Project = Project.objects.get(id=project_id)

    # 全シナリオを削除
    record_list_Scenario = Scenario.objects.filter(project=record_Project)
    for record_Scenario in record_list_Scenario:
        delete_scenario(scenario_id=record_Scenario.id)
    print("deleted all scenario")


    # 動画をクラウドから削除

    # 結合された動画を削除
    concat_movie_path = record_Project.concat_movie_path
    concat_movie_basename = os.path.basename(concat_movie_path)
    delete_file(bucket, concat_movie_basename, exist_check=True)

    # 結合されていない動画を削除
    record_list_Movie = Movie.objects.filter(project=record_Project)
    for record_Movie in record_list_Movie:
        movie_path = record_Movie.path
        key = os.path.basename(movie_path)
        delete_file(bucket, key, exist_check=True)  # クラウドの動画を削除
        record_Movie.delete()  # レコードを削除

    print("deleted all movie file and record")

    # pickleを削除
    basename = record_Project.pickle_basename
    local_path = pickle_path_local(basename)

    if os.path.exists(local_path):
        os.remove(local_path)
        print("deleted pickle : {}".format(local_path))

    record_Project.delete()
