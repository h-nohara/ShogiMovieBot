import os, sys, json, shutil, pickle, glob2
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from accounts.models.project import Project
from board.models.movie import Movie


# api
from board.src.load_save.modify import modify
from board.src.movie.generate_movie.ShogiMovieGenerator.history_to_movie import history_to_movies
from board.src.movie.generate_movie.ShogiMovieGenerator.movie_editor.split_concat_movie import concat_movie
from accounts.src.utils import generate_basename, movie_path_local, pickle_path_local
from accounts.src.utils import bucket, fname_cloud, upload_file, delete_file


@csrf_exempt
def generate_movies(request):

    print("start : generate movie")

    # data = json.loads(request.body.decode("utf-8"))
    # project_id = data["project_id"]
    # project_id = int(project_id)

    project_id = int(request.session.get("project_id"))

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
    shutil.rmtree(temporal_image_dir)  # 一時的な画像フォルダを削除

    # Movieレコードを削除
    record_list_Movie = Movie.objects.filter(project=record_Project)
    for record_Movie in record_list_Movie:
        basename = record_Movie.basename
        delete_file(bucket=bucket, key=basename, exist_check=True)  # クラウドの動画を削除
        record_Movie.delete()

    # 動画のpathを決め、Movieレコードとして保存
    ext = "mp4"
    movies = glob2.glob(os.path.abspath(os.path.join(temporal_movie_dir, "movie_*.mp4")))
    movies.sort()

    # 動画を結合する
    movie_concated = os.path.abspath(os.path.join(temporal_movie_dir, "concat_movie.mp4"))
    concat_movie(movies, movie_concated, textfile=None)  # 結合

    # movie_concated_basename = generate_basename(key+"concat", ext)
    # record_Project.concat_movie_path = fname_cloud(movie_concated_basename)  # プロジェクトレコードに保存
    # record_Project.save()

    # 結合された動画をアップロード
    concat_movie_path = record_Project.concat_movie_path
    concat_movie_basename = os.path.basename(concat_movie_path)  # クラウドのキー
    upload_file(bucket, movie_concated, concat_movie_basename)

    # 動画をアップロード＋レコードに保存
    for i in range(len(movies)):
        movie_basename = generate_basename(key+str(i), ext)
        # 動画をアップロード
        print("start upload movie [")
        # upload_movie(movies[i], movie_basename)
        upload_file(bucket, movies[i], movie_basename)
        print("finish upload movie ]")
        record_Movie = Movie(
            project = record_Project,
            basename = movie_basename,
            path = fname_cloud(movie_basename)
        )
        record_Movie.save()

    shutil.rmtree(temporal_movie_dir)  # 一時的な動画フォルダを削除

    return JsonResponse({"code" : 200})