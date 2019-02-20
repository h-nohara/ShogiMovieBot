import os, sys, json
import shutil
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project

# api
from accounts.src.utils import generate_pickle_path_local
from accounts.src.utils.generate_fname import INITIAL_PICKLE, generate_basename
from accounts.src.utils.aws_bucket import fname_cloud
from accounts.src.project.get_projects import get_projects


def copy_initial_pickle_local(path_local):

    shutil.copyfile(INITIAL_PICKLE, path_local)


def create_new_project(record_User, title):

    username = record_User.username
    n_project = len(get_projects(record_User))
    the_key = username + str(title) + str(n_project)
    pickle_path_local, pickle_basename = generate_pickle_path_local(key=the_key, get_basename=True)

    the_key_movie = the_key + "concatmovie"
    concat_movie_basename = generate_basename(key=the_key_movie, ext="mp4")

    # pickleをコピー
    copy_initial_pickle_local(pickle_path_local)

    # プロジェクトを保存
    record_Project = Project(
        user = record_User,
        title = title,
        pickle_basename = pickle_basename,
        concat_movie_path = fname_cloud(concat_movie_basename)
    )

    record_Project.save()

    print("success : create new project")


@csrf_exempt
def create_new_project_request(request):

    data = json.loads(request.body.decode("utf-8"))
    user_id = request.user.id
    # user_id = data["user_id"]
    # user_id = int(user_id)
    title = data["title"]

    record_User = User.objects.get(id=user_id)

    create_new_project(record_User, title)

    return JsonResponse({"code" : 200})