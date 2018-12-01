#!/user/bin/env python 
#-*-coding:utf-8-*-

import os, sys, subprocess, time, copy
import shutil, glob2
import numpy as np
from numpy.random import randint
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

from board.src.movie.generate_movie.ShogiMovieGenerator.call_shell import call_shell, call_check_shell



def split_one_movie(original_movie, where_to_cut, result_movie):
    
    # シェルコマンドで動画を一回だけ分割
    
    cmd_temp = "ffmpeg -y -ss {} -i {} -t {} {}"

    s = round(float(where_to_cut[0]), 4)
    e = round(float(where_to_cut[1]), 4)
        
    timelong = round((e - s), 4)
    cmd = cmd_temp.format(s, original_movie, timelong, result_movie)
    print(cmd)

    ret = subprocess.call(cmd, shell=True)
    # assert ret==0


def split_movie(original_movie, where_to_cut, split_movie_dir=None):
        
    # シェルコマンドで動画を複数に分割

    if split_movie_dir is None:
        split_movie_dir = os.path.join(os.path.dirname(original_movie), "split_movies")  # 分割した動画を保存する場所

    # 保存先のディレクトリがなければ作成
    if not os.path.exists(split_movie_dir):
        os.makedirs(split_movie_dir)
    
    cmd_temp = "ffmpeg -y -ss {} -i {} -t {} {}"

    results = []

    for i, l in enumerate(where_to_cut):

        s = round(float(l[0]), 4)
        e = round(float(l[1]), 4)
        
        timelong = round((e - s), 4)
        cmd = cmd_temp.format(s, original_movie, timelong, os.path.join(split_movie_dir, "split{0:03d}.mp4".format(i)))
        print(cmd)

        success, message = call_shell(cmd)
        results.append((success, message))

    print("cut finished")
    return results
        
        
def concat_movie(movies, result_movie, textfile=None):
    
    save_dir = os.path.dirname(result_movie)
    
    if textfile is None:
        textfile = os.path.join(save_dir, "split_movies.txt")

    # 動画の保存先のディレクトリがなければ作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 分割した動画をつなぎ合わせる

    with open(textfile, "w") as f:
        for movie in movies:
            t = "file '{}'".format(os.path.abspath(movie))
            f.write(t)
            f.write("\n")
            
    cmd = "ffmpeg -y -f concat -safe 0 -i {} -c copy {}".format(textfile, result_movie)

    print(cmd)
    success, message = call_shell(cmd)

    # 削除
    os.remove(textfile)

    return success, message



def split_concat_movie(original_movie, where_to_cut, result_movie):

    ext = os.path.basename(original_movie).split(".")[-1]
    
    temporary_save_dir = os.path.join(os.path.abspath(os.path.dirname(result_movie)), os.path.basename(original_movie).split(".")[0])
    temporary_save_dir = os.path.abspath(temporary_save_dir)
    print("temporary_save_dir : ")
    print(temporary_save_dir)

    # 分割
    results = split_movie(original_movie, where_to_cut, split_movie_dir=temporary_save_dir)
    print("finish split movie")
    print(results)

    movies = glob2.glob(os.path.join(temporary_save_dir, "*.{}".format(ext)))
    movies = [os.path.abspath(movie) for movie in movies]
    print("movies : ")
    print(movies)

    success, message = concat_movie(movies, result_movie, textfile=os.path.join(temporary_save_dir, "split_movies.txt"))
    print("finish concat movie")
    print("success : {}".format(str(success)))
    if not success:
        print(message)

    shutil.rmtree(temporary_save_dir)

    print("all_finished")

    return results, success, message

    
        
