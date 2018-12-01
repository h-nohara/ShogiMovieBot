
import os, sys

from ShogiMovieBot.settings import BASE_DIR
FONT_DIR = os.path.join(BASE_DIR, "board", "static", "fonts")


font_dict_basename = {
    "hiragino_KakuGoW6" : "hiragino_KakuGoW6.ttc",
    "hiragino_KakuGoW8" : "hiragino_KakuGoW8.ttc",
    "hiragino_MaruGo" : "hiragino_MaruGo.ttc"
}


font_dict = {key : os.path.abspath(os.path.join(FONT_DIR, font_dict_basename[key])) for key in font_dict_basename.keys()}