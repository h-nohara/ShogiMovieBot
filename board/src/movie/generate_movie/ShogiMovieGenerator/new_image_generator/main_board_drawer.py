import os, sys
from PIL import Image, ImageDraw, ImageFont

from .img_size_info import *


my_dir_path = os.path.abspath(os.path.dirname(__file__))
BOARD_IMG_PATH = os.path.join(my_dir_path, "board.png")

def get_piece_image_path(piece_name):
    my_dir_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(my_dir_path, "{}.png".format(piece_name))


class MainBoardDrawer:
    
    def __init__(self, size, loc_Piece_dict):
        
        '''
        all of size, loc : (horizontal, vertical)
        loc_Piece_dict : Board.all_pieces["main"] = {loc: Piece} Piece = {"name" : "FU", "is_sente": True}
        '''
        
        self.original_size = BOARD_IMG_MEASURE["size"]
        self.original_piece_size = PIECE_IMG_MEASURE["size"]
        self.original_square_area_size = BOARD_IMG_MEASURE["square_area_size"]
        self.original_square_area_origin = BOARD_IMG_MEASURE["square_area_origin"]

        # マス目と駒の間のスペース
        self.SQUARE_TOP_PADDING_RATIO = 0.1
        self.SQUARE_BOTTOM_PADDING_RATIO = 0.05

        self.loc_Piece_dict = loc_Piece_dict
        
        self.size = size
        self.scale = (
            self.size[0] / self.original_size[0],
            self.size[1] / self.original_size[1])
        self.square_area_size = (
            self.original_square_area_size[0] * self.scale[0],
            self.original_square_area_size[1] * self.scale[1])
        self.square_area_origin = (
            self.original_square_area_origin[0] * self.scale[0],
            self.original_square_area_origin[1] * self.scale[1])
        self.one_square_size = (
            self.square_area_size[0] / 9,
            self.square_area_size[1] / 9)

        self.common_piece_size, self.common_piece_origin_in_square = self.calc_common_piece_frame()
        

    def _get_one_square_origin(self, index=None, LocString=None):

        '''
        index: (1,1) ~ (9,9), LocString: "45"
        '''
        
        if (index is None) and (LocString is None):
            raise Exception("index and LocString are both None")
            
        if LocString is not None:
            index = self._transfer_LocString_to_LeftTopStarted(LocString)
        
        i_x = index[0]
        i_y = index[1]
        
        if (i_x<1 or i_x>9) or (i_y<1 or i_y>9):
            raise Exception("index must be in (1,1) ~ (9,9)")
            
        x = self.square_area_origin[0] + self.one_square_size[0] * (i_x-1)
        y = self.square_area_origin[1] + self.one_square_size[1] * (i_y-1)
        
        return x, y
    
    # "15"など
    def _transfer_LocString_to_LeftTopStarted(self, LocString):
        return int(10 - int(LocString[0])), int(LocString[1])

    def calc_common_piece_frame(self):

        '''
        駒に関する共通値を計算
        '''

        square_top_padding = self.one_square_size[1] * self.SQUARE_TOP_PADDING_RATIO
        piece_height = self.one_square_size[1] * (1 - (self.SQUARE_TOP_PADDING_RATIO + self.SQUARE_BOTTOM_PADDING_RATIO) )
        piece_width = piece_height * (self.original_piece_size[0] / self.original_piece_size[1])
        # if set horizontaly center
        square_left_padding = (self.one_square_size[0] - piece_width) / 2

        return (int(piece_width), int(piece_height)), (int(square_left_padding), int(square_top_padding))

    
    def calc_piece_frame(self, index=None, LocString=None, is_sente=True):

        '''
        各駒の位置を計算
        '''
        
        # マス目と駒のスペース
        origin_x, origin_y = self.common_piece_origin_in_square
        # 後手ならマス目とのスペースの上下を逆転させる
        if not is_sente:
            origin_y = self.one_square_size[1] - (origin_y+self.common_piece_size[1])
        
        square_x, square_y = self._get_one_square_origin(index=index, LocString=LocString)
        piece_x = square_x + origin_x
        piece_y = square_y + origin_y
        
        return int(piece_x), int(piece_y)


    def draw_board(self):

        board_img = Image.open(BOARD_IMG_PATH)
        return board_img.resize(self.size, resample=Image.ANTIALIAS)

    def paste_all_pieces(self, board_img, effect_locs=[]):

        '''
        board_img : 将棋盤のImageオブジェクト
        '''

        for LocString, piece_obj in self.loc_Piece_dict.items():

            if piece_obj is None:
                continue
            
            self.paste_one_piece(
                board_img=board_img,
                piece_name=piece_obj["name"],
                LocString=LocString,
                is_sente=piece_obj["is_sente"],
                with_effect = LocString in effect_locs)
        
    def paste_one_piece(self, board_img, piece_name, LocString, is_sente, with_effect=False):

        if with_effect:
            self.paste_effect(board_img, LocString)

        piece_img = Image.open(get_piece_image_path(piece_name)).resize(size=self.common_piece_size, resample=Image.ANTIALIAS)
        piece_origin = self.calc_piece_frame(LocString=LocString, is_sente=is_sente)
        if not is_sente:
            piece_img = piece_img.rotate(180)
        board_img.paste(piece_img, piece_origin, piece_img)

    def draw_all(self, effect_locs=[]):
        '''
        盤面と全ての駒を描画
        '''
        board_img = self.draw_board()
        self.paste_all_pieces(board_img, effect_locs)
        
        return board_img

    def paste_effect(self, board_img, LocString):
        origin = self._get_one_square_origin(LocString=LocString)
        hotpink = (255, 105, 180)
        effect_img = Image.new('RGB', (int(self.one_square_size[0]), int(self.one_square_size[1])), hotpink)
        board_img.paste(effect_img, [int(origin[0]), int(origin[1])])