import os, sys
from PIL import Image, ImageDraw, ImageFont

from .main_board_drawer import MainBoardDrawer
from .hand_board_drawer import HandBoardDrawer

from .img_size_info import *


def calc_aspect_kept_size(original_size, width=None, height=None, return_int=True):
    
    if (width is None) and (height is None):
        return
    if (width is not None) and (height is not None):
        return
    
    if width is not None:
        height = width * (original_size[1] / original_size[0])
    else:
        width = height * (original_size[0] / original_size[1])
    
    if return_int:
        width = int(width)
        height = int(height)

    return width, height


class Drawer:

    def __init__(self, size, all_pieces):

        '''
        all_pieces : {"main" : {}, "hand" : {"sente" : {}, "gote" : {}}}
        '''

        self.size = size
        self.all_pieces = all_pieces

    def draw_background(self):

        lavenderblush = (255, 240, 245)
        bg_img = Image.new('RGB', self.size, lavenderblush)

        return bg_img

    def draw_main_board(self, effect_locs):

        size = calc_aspect_kept_size(original_size=BOARD_IMG_MEASURE["size"], height=self.size[1], return_int=True)
        drawer = MainBoardDrawer(size=size, loc_Piece_dict=self.all_pieces["main"])
        return drawer.draw_all(effect_locs=effect_locs)

    def draw_hand_board(self, pieces, is_sente):

        size = (150, self.size[1])

        piece_height = size[1] * 0.07
        original_piece_size = PIECE_IMG_MEASURE["size"]
        piece_size = calc_aspect_kept_size(original_size=original_piece_size, height=piece_height, return_int=True)

        drawer = HandBoardDrawer(
            size=size,
            pieces=pieces,
            is_sente=is_sente,
            piece_size=piece_size)
        
        return drawer.draw_all()

    def draw_all(self, effect_locs=[]):

        bg_img = self.draw_background()

        main_board_img = self.draw_main_board(effect_locs=effect_locs)
        main_board_size = calc_aspect_kept_size(original_size=BOARD_IMG_MEASURE["size"], height=self.size[1], return_int=True)
        main_board_x = (self.size[0] - main_board_size[0]) / 2
        main_board_y = 0
        bg_img.paste(main_board_img, (int(main_board_x), int(main_board_y)), main_board_img)

        space_hand_main = 10

        for is_sente, sente_or_gote in zip([True, False], ["sente", "gote"]):

            hand_board_img = self.draw_hand_board(pieces=self.all_pieces["hand"][sente_or_gote], is_sente=is_sente)
            hand_table_size = (150, self.size[1])
            hand_board_y = 0
            if is_sente:
                hand_board_x = main_board_x + main_board_size[0] + space_hand_main
            else:
                hand_board_x = main_board_x - (hand_table_size[0] + space_hand_main)
            bg_img.paste(hand_board_img, (int(hand_board_x), int(hand_board_y)))

        return bg_img
         
            