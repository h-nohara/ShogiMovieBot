 #!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, copy

from .piece import Piece
from .util import *
import time

import multiprocessing
import numpy as np
from multiprocessing import Process, Queue, Pool
from itertools import chain


'''
potential_moves : 駒が本来動ける方向
natural_moves : 王手されていることを考えない、可能な指し手
legal_moves : 可能な指し手
'''



def get_legal_moves(Board, loc=None):
    
    # s = time.time()
    
    # natural_movesを取得
    
    natural_moves = get_all_natural_moves(Board)

    # print("natural")
    # print(natural_moves)

    # e = time.time()

    
    # もしそれぞれのnatural_moveを行った場合、玉が相手の駒にattackされている状態になっていないかチェックする

    # 玉の位置を探す
    sente_or_gote = "sente" if Board.is_sente else "gote"

    for piece in Board.all_pieces["main"].values():
        if piece is not None:
            if (piece.name == "OU") and (piece.is_sente == Board.is_sente):
                loc_of_OU = piece.loc

    legal_moves = []

#    print(natural_moves)

#    print("="*20)
#    print(Board.all_pieces["main"]["99"].loc)

    # ss = time.time()

    for move in natural_moves:

        assert (len(move) == 4) or (len(move) == 5)
        board_copy = copy.deepcopy(Board)
        
        # 移動
        if move[:2] not in PieceName_Hand:
            
            original_piece = Board.all_pieces["main"][move[:2]]
            
            assert original_piece is not None

            # 駒を移動
            board_copy.all_pieces["main"][move[:2]] = None
            new_piece = Piece(name=original_piece.name, is_sente=original_piece.is_sente, loc=move[2:4])
            board_copy.all_pieces["main"][move[2:4]] = copy.deepcopy(new_piece)

            if new_piece.name == "OU":
                # print("yes")
                loc_of_OU_now = new_piece.loc
            else:
                # print("no")
                loc_of_OU_now = loc_of_OU

        # 打ち手
        else:
            loc_of_OU_now = loc_of_OU
            the_piece_name = move[:2]
            board_copy.all_pieces["hand"][sente_or_gote][the_piece_name] -= 1
            board_copy.all_pieces["main"][move[2:4]] = copy.deepcopy(Piece(name=the_piece_name, is_sente=board_copy.is_sente, loc=move[2:4]))

        # 手番を交代
        board_copy.is_sente = not board_copy.is_sente

        natural_moves_enemy = get_all_natural_moves(board_copy)
        natural_moves_dest_enemy = [move[2:4] for move in natural_moves_enemy]

        if loc_of_OU_now not in natural_moves_dest_enemy:
            legal_moves.append(move)
        # else:
        #     print("natural moves dest enem")
        #     # print(move) #######
        #     # print("board copy")
        #     # print(board_copy)
        #     print(natural_moves_enemy)
        #     print("loc of ou : {}".format(loc_of_OU_now))

        # board_copy = None

    # ee = time.time()

    # print("legal")
    # print(legal_moves)

#    print(e -s)
#    print(ee-ss)

    return legal_moves



def get_all_natural_moves(Board, loc=None):
    
    '''
    loc(str) : Noneなら全ての移動、指定されればその位置の駒の移動だけ
    '''
    
    if loc is None:

        # 移動
        natural_moves_move = get_all_natural_moves_move(Board)
        # 手駒
        natural_moves_put = get_all_natural_moves_put(Board)

        # 移動と打ち手を合わせる
        all_natural_moves = natural_moves_move + natural_moves_put


    else:
        # 引数の駒が手駒かどうか（locで確認）確認して
        raise ValueError("not useable")

    return all_natural_moves



def get_all_natural_moves_move(Board):

    # Board = copy.deepcopy(Board)

    is_sente = Board.is_sente

    # 全ての味方の駒の、全ての移動可能な場所を洗い出す
    natural_moves_move = []

    for key in Board.all_pieces["main"].keys():
        piece = Board.all_pieces["main"][key]
    # for piece in Board.all_pieces["main"].values():
        if piece is not None:
            if piece.is_sente == is_sente:

                if piece.loc is None:
                    print("oh no!")
                    print(key)
                    print(piece.__dict__)
                    raise ValueError("aa")

                natural_moves_move += get_natural_moves_move(piece, Board)

    return natural_moves_move


def get_all_natural_moves_put(Board):

    # Board = copy.deepcopy(Board)

    is_sente = Board.is_sente
    natural_moves_put = []

    if is_sente:
        pieces_in_hand = Board.all_pieces["hand"]["sente"]
    else:
        pieces_in_hand = Board.all_pieces["hand"]["gote"]

    for piece_name in pieces_in_hand.keys():
        if pieces_in_hand[piece_name] > 0:
            piece = copy.deepcopy(Piece(name=piece_name, is_sente=is_sente))
            natural_moves_put += get_natural_moves_put(piece, Board)

    return natural_moves_put
        
    

def can_move_to(Board, dest, is_sente):
    
    '''
    ・そこに味方の駒がないか
    ・１〜９の間の位置か
    をチェック

    dest(str) : 移動先のloc

    return(bool) : そこへ動けるかどうか

    >>> can_move_to(board, "55", True)
    '''

    if (len(dest) != 2) and (len(dest) != 3):
        print()
        print(dest)
        print()
        raise ValueError("oh my")

    if (len(dest) == 3) and (dest[-1] != "+"):
        return False

    dest = dest[:2]

    # 盤上に収まっていなかったら
    if (int(dest[0]) > 9) or (int(dest[0]) < 1) or (int(dest[1]) > 9) or (int(dest[1]) < 1):
        return False

    piece = Board.all_pieces["main"][dest]

    # 移動先に味方の駒があったら
    if (piece is not None) and (piece.is_sente == is_sente):
        return False

    # 移動先に敵の駒があったら
    elif (piece is not None) and (piece.is_sente != is_sente):
        return 1

    else:
        return True
        
    

def get_natural_moves_move(Piece, Board):
    
    '''
    移動可能な場所を示す（王手による影響は考えない）
    '''
    
    loc = Piece.loc
    col_num = int(loc[0])
    row_num = int(loc[1])
    is_sente = Piece.is_sente

    assert is_sente == Board.is_sente

    potential_dests = []  # この駒が本来動ける方向

    if Piece.name == "FU":

        if is_sente:
            dest = loc[0] + str(int(loc[1]) - 1)
        else:
            dest = loc[0] + str(int(loc[1]) + 1)
        
        potential_dests = [dest]


    elif Piece.name == "KY":

        if is_sente:
            
            row_num = row_num - 1
            while row_num >= 1:
                dest = loc[0] + str(row_num)
                if can_move_to(Board, dest, is_sente) is True:
                    potential_dests.append(dest)
                    row_num -= 1
                elif can_move_to(Board, dest, is_sente) == 1:
                    potential_dests.append(dest)
                    break
                else:
                    break
                
        else:
            for row_num in range(row_num+1, 10):
                dest = loc[0] + str(row_num)
                if can_move_to(Board, dest, is_sente) is True:
                    potential_dests.append(dest)
                elif can_move_to(Board, dest, is_sente) == 1:
                    potential_dests.append(dest)
                    break
                else:
                    break

    elif Piece.name == "KE":
        
        if is_sente:
            potential_dests = [str(col_num-1) + str(row_num-2), str(col_num+1) + str(row_num-2)]
        else:
            potential_dests = [str(col_num-1) + str(row_num+2), str(col_num+1) + str(row_num+2)]

    elif Piece.name == "GI":
        
        if is_sente:
            potential_dests = [
                str(col_num - 1) + str(row_num - 1),
                str(col_num) + str(row_num - 1),
                str(col_num + 1) + str(row_num - 1),
                str(col_num - 1) + str(row_num + 1),
                str(col_num + 1) + str(row_num + 1)
            ]

        else:
            potential_dests = [
                str(col_num - 1) + str(row_num + 1),
                str(col_num) + str(row_num + 1),
                str(col_num + 1) + str(row_num + 1),
                str(col_num - 1) + str(row_num - 1),
                str(col_num + 1) + str(row_num - 1)
            ]

    elif (Piece.name == "KI") or (Piece.name == "TO") or (Piece.name == "NY") or (Piece.name == "NK") or (Piece.name == "NG"):
        
        if is_sente:
            potential_dests = [
                str(col_num - 1) + str(row_num - 1),
                str(col_num) + str(row_num - 1),
                str(col_num + 1) + str(row_num - 1),
                str(col_num - 1) + str(row_num),
                str(col_num + 1) + str(row_num),
                str(col_num) + str(row_num + 1),
            ]

        else:
            potential_dests = [
                str(col_num - 1) + str(row_num + 1),
                str(col_num) + str(row_num + 1),
                str(col_num + 1) + str(row_num + 1),
                str(col_num - 1) + str(row_num),
                str(col_num + 1) + str(row_num),
                str(col_num) + str(row_num - 1)
            ]

    elif Piece.name == "OU":
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0) and (j == 0):
                    continue
                else:
                    c = col_num + i
                    r = row_num + j
                    if ((c > 0) and (c < 10) and (r > 0) and (r<10)):
                        potential_dests.append(str(c) + str(r))

    
    elif (Piece.name == "KA") or (Piece.name == "UM"):
                    
        # 左下
        c = col_num + 1
        r = row_num + 1
        while (c < 10) and (r < 10):
            dest = str(c) + str(r)
            if can_move_to(Board, dest, is_sente) is True:
                potential_dests.append(dest)
                c += 1
                r += 1
            elif can_move_to(Board, dest, is_sente) == 1:
                potential_dests.append(dest)
                break
            else:
                break

        # 左上
        c = col_num + 1
        r = row_num - 1
        while (c < 10) and (r > 0):
            dest = str(c) + str(r)
            if can_move_to(Board, dest, is_sente) is True:
                potential_dests.append(dest)
                c += 1
                r -= 1
            elif can_move_to(Board, dest, is_sente) == 1:
                potential_dests.append(dest)
                break
            else:
                break

        # 右下
        c = col_num - 1
        r = row_num + 1
        while (c > 0) and (r < 10):
            dest = str(c) + str(r)
            if can_move_to(Board, dest, is_sente) is True:
                potential_dests.append(dest)
                c -= 1
                r += 1
            elif can_move_to(Board, dest, is_sente) == 1:
                potential_dests.append(dest)
                break
            else:
                break

        # 右上
        c = col_num - 1
        r = row_num - 1
        while (c > 0) and (r > 0):
            dest = str(c) + str(r)
            if can_move_to(Board, dest, is_sente) is True:
                potential_dests.append(dest)
                c -= 1
                r -= 1
            elif can_move_to(Board, dest, is_sente) == 1:
                potential_dests.append(dest)
                break
            else:
                break

        # 横
        if Piece.name == "UM":
            potential_dests += [
                str(col_num+1) + str(row_num),  # 左
                str(col_num) + str(row_num-1),  # 上
                str(col_num) + str(row_num+1),  # 下
                str(col_num-1) + str(row_num),  # 右
            ]

    elif (Piece.name == "HI") or (Piece.name == "RY"):
        
        # 左
        c = col_num + 1
        while c < 10:
            dest = str(c) + str(row_num)
            if can_move_to(Board, dest, is_sente) is True:
                potential_dests.append(dest)
                c += 1
            elif can_move_to(Board, dest, is_sente) == 1:
                potential_dests.append(dest)
                break
            else:
                break

        # 右
        c = col_num - 1
        while c > 0:
            dest = str(c) + str(row_num)
            if can_move_to(Board, dest, is_sente) is True:
                potential_dests.append(dest)
                c -= 1
            elif can_move_to(Board, dest, is_sente) == 1:
                potential_dests.append(dest)
                break
            else:
                break

        # 上
        r = row_num - 1
        while r > 0:
            dest = str(col_num) + str(r)
            if can_move_to(Board, dest, is_sente) is True:
                potential_dests.append(dest)
                r -= 1
            elif can_move_to(Board, dest, is_sente) == 1:
                potential_dests.append(dest)
                break
            else:
                break
        
        # 下
        r = row_num + 1
        while r < 10:
            dest = str(col_num) + str(r)
            if can_move_to(Board, dest, is_sente) is True:
                potential_dests.append(dest)
                r += 1
            elif can_move_to(Board, dest, is_sente) == 1:
                potential_dests.append(dest)
                break
            else:
                break

        # 斜め横
        if Piece.name == "RY":
            potential_dests += [
                str(col_num+1) + str(row_num+1),  # 左下
                str(col_num+1) + str(row_num-1),  # 左上
                str(col_num-1) + str(row_num+1),  # 右下
                str(col_num-1) + str(row_num-1),  # 右上
            ]


    natural_moves = []

    for dest in potential_dests:

        # 移動先が盤内ではないものは無視
        if (dest[:2] == "10") or (dest[-2:] == "10"):
            continue

        if can_move_to(Board, dest, is_sente):

            # 歩か香は、最終段以外なら成らずに進める
            if (Piece.name == "FU") or (Piece.name == "KY"):
                if dest[1] != "9":
                    natural_moves.append(loc + dest)
            # 桂馬は、最終段とその手前以外なら成らずに進める
            elif (Piece.name == "KE"):
                if (dest[1] != "8") and (dest[1] != "9"):
                    natural_moves.append(loc + dest)
            # それ以外の駒は、無条件で成らずに進める
            else:
                natural_moves.append(loc + dest)

            # 成ることができれば、その手も加える（移動先か移動元が敵陣なら成ることができる）
            if is_land_of_enemy(dest, is_sente) or is_land_of_enemy(loc, is_sente):
                if Piece.name in PieceName_Hand:
                    natural_moves.append(loc + dest + "+")
                

    return natural_moves


def is_land_of_enemy(loc, is_sente):

    '''
    指し手にとって、その場所が敵陣かどうかを返す

    loc(str) : 対象の場所
    is_sente(bool) : 対象の指し手

    return(bool)
    '''

    assert len(loc) == 2
    
    row_num = int(loc[1])
    assert (row_num > 0) and (row_num < 10)

    # 後手の場合
    if (row_num >= 7) and (not is_sente):
        return True

    # 先手の場合
    elif (row_num <= 3) and is_sente:
        return True

    else:
        return False



def get_natural_moves_put(Piece, Board):

    '''
    Piece(Piece) : 持ち駒
    '''

    is_sente = Piece.is_sente
    piece_name = Piece.name
    assert is_sente == Board.is_sente

    potential_moves_put = []

    # 駒が置かれていない場所を全て列挙

    for loc in Board.all_pieces["main"].keys():
        piece = Board.all_pieces["main"][loc]
        if piece is None:
            potential_moves_put.append(loc)


    natural_moves_put = []
            
    if piece_name == "FU":
        
        for loc in potential_moves_put:
            
            # 最終段かどうか確認
            if (is_sente and (loc[1] == "1")) or ((not is_sente) and (loc[1] == "9")):
                continue

            # ２歩を確認
            else:
                is_nifu = False
                
                col = loc[0]
                for row_num in range(1, 10):
                    the_piece = Board.all_pieces["main"][col + str(row_num)]
                    if the_piece is not None:
                        if (the_piece.name == "FU") and (the_piece.is_sente is is_sente):
                            is_nifu = True
                            break
                
                if not is_nifu:
                    natural_moves_put.append(loc)


    elif piece_name == "KY":
        
        for loc in potential_moves_put:
            
            # 最終段かどうか確認
            if (is_sente and (loc[1] == "1")) or ((not is_sente) and (loc[1] == "9")):
                continue
            else:
                natural_moves_put.append(loc)


    elif piece_name == "KE":
        
        for loc in potential_moves_put:
            
            # 最終段かどうか確認
            if (is_sente and ((loc[1] == "1") or (loc[1] == "2"))) or ((not is_sente) and ((loc[1] == "8") or (loc[1] == "9"))):
                continue
            else:
                natural_moves_put.append(loc)

    else:
        natural_moves_put = potential_moves_put

    natural_moves_put = [piece_name + loc for loc in natural_moves_put]

    return natural_moves_put
