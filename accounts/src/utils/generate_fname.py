import os, sys, pytz, hashlib
from datetime import datetime

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ShogiMovieBot.settings import BASE_DIR  # プロジェクトディレクトリ

# pickleファイルの保存場所
PICKLE_DIR = os.path.abspath(os.path.join(BASE_DIR, "board", "static", "pickle"))
PICKLE_USER_DIR = os.path.abspath(os.path.join(PICKLE_DIR, "user"))
PICKLE_DEFAULT_DIR = os.path.abspath(os.path.join(PICKLE_DIR, "default"))
INITIAL_PICKLE = os.path.abspath(os.path.join(PICKLE_DEFAULT_DIR, "initial.pickle"))

# 動画の保存場所
MOVIE_DIR = os.path.abspath(os.path.join(BASE_DIR, "board", "static", "movie"))
MOVIE_USER_DIR = os.path.abspath(os.path.join(MOVIE_DIR, "user"))

# db


# api



def get_TimeStringSeries():

    now = datetime.now(pytz.timezone('Asia/Tokyo'))
    string = now.strftime("%Y%m%d%H%M%S%f")
    return string


def get_sha256(string):

    hashed = hashlib.sha256(string.encode("utf-8")).hexdigest()
    return hashed


def generate_basename(key, ext):
    
    key = str(key) + get_TimeStringSeries()
    hashed = get_sha256(key)
    fname = "{}.{}".format(hashed, ext)
    return fname


# pickle

def pickle_path_local(basename):
    
    return os.path.abspath(os.path.join(PICKLE_USER_DIR, basename))


def generate_pickle_path_local(key, get_basename=False):

    ext = "pickle"
    basename = generate_basename(key, ext)
    pickle_path = os.path.abspath(os.path.join(PICKLE_USER_DIR, basename))
    
    if get_basename:
        return pickle_path, basename

    return pickle_path


# 動画

def movie_path_local(basename):

    return os.path.abspath(os.path.join(MOVIE_USER_DIR, basename))


# def generate_fname_replicate(fname):

#     dirname = os.path.dirname(fname)
#     ext = fname.split(".")[-1]
#     key = os.path.basename(fname)
#     result_basename = generate_basename(key, ext)
#     result = os.path.join(dirname, result_basename)
#     return result
