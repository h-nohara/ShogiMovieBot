#!/user/bin/env python 
# -*- coding: utf-8 -*-

import os, sys, copy, shutil
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from .plot_board import Plot
from .util import get_abspath

from .new_image_generator.whole_drawer import Drawer

# api
from board.src.movie.generate_movie.font import font_dict
from board.src.movie.generate_movie.ShogiMovieGenerator.image_editor.make_WordImage import make_WordImage
from board.src.movie.generate_movie.ShogiMovieGenerator.image_editor.overlaid_image import overlaid_handler
from board.src.movie.generate_movie.ShogiMovieGenerator.images_to_movie import images_to_movie


'''
recorder = ImageNameRecorder("img/")
history_to_images(history, recorder)
'''


def draw_boad(board, save_name, light_up_locs=False, mark_locs=False):
        
    '''
    盤面画像を保存する
    オプションで背景に色をつける

    light_up_locs(list(tuple)) : 背景に色をつける位置

    >>> self.draw_board(light_up_locs=["55", "34"], mark_locs=[])
    '''

    drawer = Drawer(size=(1920, 1080), all_pieces=board["all_pieces"])
    if light_up_locs is not False:
        light_up_locs = [str(loc[0])+str(loc[1]) for loc in light_up_locs] # [(1,2), ] -> ["12", ]
    else:
        light_up_locs = []
    img = drawer.draw_all(effect_locs=light_up_locs)
    img.save(save_name)

    ##################
    
    # board_plot = Plot(board)

    # # 盤面
    # board_plot.plot_board()


    # # マーキング
    # if light_up_locs:
    #     light_up_locs = [(int(loc_str[0]), int(loc_str[1])) for loc_str in light_up_locs]  # ["11", ...] -> [(1, 1), ...]
    #     board_plot.plot_marking(locs=light_up_locs, shape="square")
    # if mark_locs:
    #     mark_locs = [(int(loc_str[0]), int(loc_str[1])) for loc_str in mark_locs]  # ["11", ...] -> [(1, 1), ...]
    #     board_plot.plot_marking(locs=mark_locs, shape="circle")
    
    # # 駒
    # board_plot.plot_pieces()
    # board_plot.plot_komadai()
    # board_plot.plot_mochigoma()

    # board_plot.save_pic(save_name)  # 保存
    # plt.close()


# todo : 複数の文字画像を扱えるようにする
def draw_text(message, base_image_path, word_image_path):
    
    # 最初に文字画像を生成

    # font_size = 50
    font_size = 100
    len_one_row = 10

    text = message["text"]

    # テキストを一行の文字数制限ごとに分割
    
    text_each_row = []
    rows_original = text.split("\n")  # ユーザが入力したままの行ごと
    for row in rows_original:
        text_split = [row[i: i+len_one_row] for i in range(0, len(row), len_one_row)]  # 文字数制限ごとに分割
        for chunk in text_split:
            if chunk != "":
                text_each_row.append(chunk)

    n_row = len(text_each_row)
    text_with_br = "\n".join(text_each_row)  # 改行させる

    print("[ start : make wordimage")

    # make_WordImage(
    #     word = text, 
    #     fontsize = font_size, 
    #     fontfile = font_dict["hiragino_KakuGoW6"], 
    #     num_color = 2, 
    #     # colors = ["white", "'#6699ff'"],
    #     colors = ["white", "'#FF1493'"],
    #     stroke_ws = [2],
    #     result_image = word_image_path,
    #     W = font_size * (1 + len(text)),
    #     H = font_size * 1.3
    # )

    # 改行ありバージョン

    make_WordImage(
        word = text_with_br,
        fontsize = font_size,
        fontfile = font_dict["hiragino_KakuGoW8"],
        num_color = 3,
        # colors = ["white", "'#6699ff'"],
        colors = ["white", "'#FF1493'", "white"],
        stroke_ws = [15, 8], # 3.5
        result_image = word_image_path,
        W = font_size * (1 + len_one_row),
        H = font_size * 1.3 * n_row
    )

    print("finish : make wordimage ]")

    # 盤面画像に貼り付ける
    overlaid_handler(base_image_path, [word_image_path], base_image_path)
    print("finish : overlaid wordimage ]")



def action_to_image(action, save_name):
    
    board = action["board_state"]

    if "message" in action.keys():

        message = action["message"]

        light_up_locs = False
        mark_locs = False

        if "light_up" in message.keys():
            if message["light_up"]:
                light_up_locs = message["light_up"]

        if "mark" in message.keys():
            if message["mark"]:
                mark_locs = message["mark"]


        draw_boad(board=board, light_up_locs=light_up_locs, mark_locs=mark_locs, save_name=save_name)

        if "text" in message.keys():
            word_image_path = os.path.join(os.path.dirname(save_name), "word.png")
            draw_text(message, save_name, word_image_path)



    elif "fly_to" in action.keys():

        draw_boad(board=board, save_name=save_name)

    elif "move" in action.keys():

        move = action["move"]
        pos_after = move[2:]  # 動き先の位置
        assert (len(pos_after) == 2) or ((len(pos_after) == 3) and pos_after[-1]=="+")
        draw_boad(board=board, light_up_locs=[(int(pos_after[0]), int(pos_after[1]))], save_name=save_name)



def history_to_images(history, recorder):

    '''
    save_dir（ImageNameRecorderが管理）の中に、順番に画像を保存していく

    recoder(ImageNameRecorder)
    '''

    for action in history:

        # シナリオアクション以外だったら、画像を生成
        if "scenarios" not in action.keys():
            save_name = recorder.next()

            # initiialの時
            if "move" in action.keys():
                if action["move"] == "initial":
                    draw_boad(action["board_state"], save_name)
                    continue

            action_to_image(action, save_name)

        # シナリオアクションだったら
        else:

            board_before_branch = action["board_state"]

            # サブシナリオを順番にみていく
            for mini_sc in action["scenarios"]:

                save_name = recorder.next(True)
                draw_boad(board_before_branch, save_name)  # 分岐の直前の状態を毎回画像に

                # 分岐の後にメッセージを入れる
                # save_name = recorder.next(True)
                # message_action = {
                #     "board_state" : board_before_branch,
                #     "message" : {"text" : "分岐前に戻ります"}
                # }
                # action_to_image(message_action, save_name)

                history_to_images(mini_sc, recorder)  # 分岐後を順番に画像に


def history_to_InitBoard_image(history, result_image):

    action = history[0]
    draw_boad(action["board_state"], result_image)



def history_to_movies(history, save_dir_img, save_dir_movie):

    '''
    画像の一覧から複数の動画に生成する。
    各動画を生成する際に、一時的なフォルダを作成し、その中に動画用の画像をコピーして、動画を生成する。
    '''

    recorder = ImageNameRecorder(save_dir_img)
    history_to_images(history, recorder)

    # [0, 12, 20, 最後]　のような形式で、画像の区切りをリストに
    cut_head_numbers = [0]
    for fname in recorder.cut_heads:
        number = int(os.path.basename(fname).split(".")[0].split("_")[-1])
        cut_head_numbers.append(number)
    cut_head_numbers.append(recorder.counter)

    chunk_imges_dir = os.path.join(save_dir_img, "temporary_chunks")
    if os.path.exists(chunk_imges_dir):
        shutil.rmtree(chunk_imges_dir)

    # 各動画を生成する
    for i in range(len(cut_head_numbers) - 1):

        head = cut_head_numbers[i]
        after_tail = cut_head_numbers[i+1]

        os.makedirs(chunk_imges_dir)

        # 今回の動画用の画像を新しいフォルダにコピーする
        for j, num in enumerate(range(head, after_tail)):
            img_to_copy = os.path.join(save_dir_img, recorder.base_temp_name.format(num))
            shutil.copy(img_to_copy, os.path.join(chunk_imges_dir, "img_{0:03d}.png".format(j)))

        # 動画を生成
        img_path_temp = os.path.join(chunk_imges_dir, "img_%03d.png")
        result_name = os.path.join(save_dir_movie, "movie_{0:03d}.mp4".format(i))
        images_to_movie(load_dir=chunk_imges_dir, img_path_temp=img_path_temp, result_name=result_name)

        shutil.rmtree(chunk_imges_dir)



class ImageNameRecorder:

    def __init__(self, save_dir):

        self.save_dir = save_dir
        self.base_temp_name = "img_{0:03d}.png"

        self.counter = 0
        self.cut_heads = []

    
    def next(self, is_cut_head=False):

        img_path = os.path.join(self.save_dir, self.base_temp_name.format(self.counter))
        self.counter += 1
        
        if is_cut_head:
            self.cut_heads.append(img_path)

        return img_path
