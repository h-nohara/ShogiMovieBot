
import os, sys, copy

# api
from board.src.movie.generate_movie.shogi_api.board import Board

def kifu_to_history(hands, hands_str):
    
    '''
    hands : 標準形の指し手のリスト
    '''
    
    shogi_board = Board()
    history = []
    
    # 初期盤面
    initial_action = {
        "move" : "initial",
        "move_str" : "initial",
        "board_state" : {"all_pieces" : copy.deepcopy(shogi_board.all_pieces)}
    }
    loc_piece_dict = initial_action["board_state"]["all_pieces"]["main"]
    # Pieceオブジェクトから辞書へ
    for loc in loc_piece_dict.keys():
        piece = loc_piece_dict[loc]
        if piece is not None:
            loc_piece_dict[loc] = {"name" : piece.name, "loc" : piece.loc, "is_sente" : piece.is_sente}
    history.append(initial_action)

    for hand, hand_str in zip(hands, hands_str):
        
        # print(hand, hand_str)
        
        action = {"move" : None, "board_state" : None}
            
        shogi_board.move(hand)  # 将棋盤を更新
        
        action["move"] = hand
        action["move_str"] = hand_str
        action["board_state"] = {"all_pieces" : copy.deepcopy(shogi_board.all_pieces)}
        
        # Pieceオブジェクトから、辞書へ
        loc_piece_dict = action["board_state"]["all_pieces"]["main"]
        for loc in loc_piece_dict.keys():
            piece = loc_piece_dict[loc]
            if piece is not None:
                loc_piece_dict[loc] = {"name" : piece.name, "loc" : piece.loc, "is_sente" : piece.is_sente}

        history.append(action)

    return history
