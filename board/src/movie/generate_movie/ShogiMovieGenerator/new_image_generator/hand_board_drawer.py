import os, sys
from PIL import Image, ImageDraw, ImageFont

from .img_size_info import *

def get_piece_image_path(piece_name):
    my_dir_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(my_dir_path, "{}.png".format(piece_name))

def add_text_to_image(img, text, font_path, font_size, font_color, origin):
    
    font = ImageFont.truetype(font=font_path, size=font_size)
    
    draw = ImageDraw.Draw(img)
    
#     if draw.textsize(text, font=font)[0] > max_length:
#         while draw.textsize(text + '…', font=font)[0] > max_length:
#             text = text[:-1]
#         text = text + '…'

    draw.text(origin, text, font_color, font=font)


class HandBoardDrawer:

    def __init__(self, size, piece_size, pieces, is_sente, left_padding=10, bottom_padding=30, piece_space=20):

        '''
        pieces: {name: number}
        left_padding: 盤面方向へのパディング（後手の場合は右側）
        bottom_padding: 駒の底方向へのパディング（駒が裏返しの場合は上側）
        piece_space: 駒の間隔
        '''

        self.original_piece_size = PIECE_IMG_MEASURE["size"]

        self.size = size
        self.piece_size = piece_size
        self.pieces = pieces
        self.is_sente = is_sente
        self.left_padding = left_padding
        self.bottom_padding = bottom_padding
        self.piece_space = piece_space


    def draw_board(self):

        peru = (205, 133, 63)
        board_img = Image.new('RGB', self.size, peru)

        return board_img.resize(self.size, resample=Image.ANTIALIAS)

    def draw_all(self):
        board_img = self.draw_board()
        self.paste_all_pieces(board_img)
        return board_img


    def paste_all_pieces(self, board_img):

        order_piece_names_hand = ["FU", "KY", "KE", "GI", "KI", "KA", "HI"]

        index = 0
        for piece_name in order_piece_names_hand:
            if not piece_name in self.pieces.keys():
                continue
            number = self.pieces[piece_name]
            if number >= 1:
                self.paste_one_piece(
                    board_img = board_img,
                    piece_name = piece_name,
                    number = number,
                    index = index)
                index += 1
        
    def paste_one_piece(self, board_img, piece_name, number, index):

        '''
        駒画像とその枚数表示
        number: 枚数
        index : 下から何番目に重ねるか、0〜
        '''
    
        piece_img = Image.open(get_piece_image_path(piece_name)).resize(size=self.piece_size, resample=Image.ANTIALIAS)
        font_path = "/System/Library/Fonts/SFCompactRounded-Black.otf"

        if self.is_sente:
            piece_top = self.size[1] - (self.bottom_padding + (index+1) * self.piece_size[1] + index * self.piece_space )
            piece_x = self.left_padding
            number_x = self.left_padding+self.piece_size[0]
        
        else:
            piece_img = piece_img.rotate(180)
            piece_top = self.bottom_padding + index * (self.piece_size[1] + self.piece_space )
            space_width_for_number = 25
            piece_x = self.size[0] - (self.left_padding + self.piece_size[0]) - space_width_for_number
            number_x = self.size[0] - self.left_padding - space_width_for_number

        board_img.paste(piece_img, (piece_x, piece_top), piece_img)
        green = (0, 255, 127)
        add_text_to_image(
            img = board_img,
            text = str(number),
            font_path = font_path,
            font_size = 50,
            font_color = green,
            origin = (number_x, piece_top) )