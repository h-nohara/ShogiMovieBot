import os, sys, json, shutil, pickle, glob2
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project
from board.models.movie import Movie
from board.models.image import Image


# api
from board.src.load_save.modify import modify
from board.src.movie.generate_movie.ShogiMovieGenerator.history_to_movie import history_to_InitBoard_image
from accounts.src.utils import generate_basename, movie_path_local, pickle_path_local
from accounts.src.utils import bucket, fname_cloud, upload_file, delete_file


def generate_InitBoard_image(project_id):

    '''
    画像を生成して、データベースに登録＋クラウドにアップロード
    '''

    print("start : generate InitBoard_image")

    # if request.method == "GET":
    #     project_id = int(request.session.get("project_id"))

    # else:
    #     data = json.loads(request.body.decode("utf-8"))
    #     project_id = data["project_id"]
    #     project_id = int(project_id)
    
    record_Project = Project.objects.get(id=project_id)


    # 盤面情報をpickleから読み出し
    pickle_basename = record_Project.pickle_basename
    pickle_path = pickle_path_local(pickle_basename)
    with open(pickle_path, mode="rb") as f:
        result = pickle.load(f)
        history = result["history"]
    

    # 一時的な画像保存フォルダを作成
    key = str(project_id)+record_Project.title+"InitBoardImage"
    temporal_image_dir = movie_path_local("temporal_image_"+key)
    if os.path.exists(temporal_image_dir):
        shutil.rmtree(temporal_image_dir)
    os.makedirs(temporal_image_dir)

    # 画像のローカルパス
    path_local = os.path.join(temporal_image_dir, "InitBoard.png")

    # 画像を生成
    history_to_InitBoard_image(history=history, result_image=path_local)

    # Imageレコードの中に、このプロジェクトの初期盤面画像があるか確認
    record_list_Image = Image.objects.filter(project=record_Project, kind="InitBoard")

    if len(record_list_Image) == 0:

        basename = generate_basename(key=key, ext="png")
        path_cloud = fname_cloud(basename)

        record_Image = Image(
            project = record_Project,
            path = path_cloud,
            basename = basename,
            kind = "InitBoard"
        )
        record_Image.save()

    else:
        record_Image = record_list_Image[0]
        path_cloud = record_Image.path
        basename = os.path.basename(path_cloud)


    # 画像をアップロード
    upload_file(bucket, path_local, basename)


    # 一時的な画像保存フォルダを削除
    shutil.rmtree(temporal_image_dir)

    return path_cloud