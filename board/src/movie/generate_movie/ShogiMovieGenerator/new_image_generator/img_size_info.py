import os, sys


BOARD_IMG_MEASURE = {
    "size" : (915, 915),
    "square_area_size" : (751, 751),
    "square_area_origin" : (82, 82)
}

PIECE_IMG_MEASURE = {
    "size" : (240, 280)
}


SQUARE_PIECE_RELATIVE = {
    "origin_ratio" : (0.05, None),
    "piece_size_ratio" : (0.92, None)
}


class _MAIN_BOARD_DRAWER:
    
    def __init__(self, size):
        
        """
        all of size, loc : (horizontal, vertical)
        """
        
        self.original_size = BOARD_IMG_MEASURE["size"]
        self.original_piece_size = PIECE_IMG_MEASURE["size"]
        self.original_square_area_size = BOARD_IMG_MEASURE["square_area_size"]
        self.original_square_area_origin = BOARD_IMG_MEASURE["square_area_origin"]
        
        self.size = size
        self.scale = (
            self.size[0] / self.original_size[0],
            self.size[1] / self.original_size[1])
        self.square_area_size = (
            self.original_square_area_size[0] * self.scale[0],
            self.original_square_area_size[1] * self.scale[1])
        self.square_area_origin = (
            self.original_square_area_origin[0] * self.scale[0],
            self.original_square_area_origin[1] * self.scale[1]
        )
        self.one_square_size = (
            self.square_area_size[0] / 9,
            self.square_area_size[1] / 9)

    # index: (1,1) ~ (9,9), LocString: "45"
    def _get_one_square_origin(self, index=None, LocString=None):
        
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
    
    def calc_piece_frame(self, index=None, LocString=None):
        
        # マス目と駒のスペース
        SQUARE_TOP_PADDING_RATIO = 0.1
        SQUARE_BOTTOM_PADDING_RATIO = 0.05
        
        square_top_padding = self.one_square_size[1] * SQUARE_TOP_PADDING_RATIO
        
        piece_height = self.one_square_size[1] * (1-SQUARE_TOP_PADDING_RATIO-SQUARE_BOTTOM_PADDING_RATIO)
        piece_width = piece_height * (self.original_piece_size[0] / self.original_piece_size[1])
        
        # if set horizontaly center
        square_left_padding = (self.one_square_size[0] - piece_width) / 2
        
        square_x, square_y = self._get_one_square_origin(index=index, LocString=LocString)
        piece_x = square_x + square_left_padding
        piece_y = square_y + square_top_padding
        
        return (int(piece_x), int(piece_y)), (int(piece_width), int(piece_height))