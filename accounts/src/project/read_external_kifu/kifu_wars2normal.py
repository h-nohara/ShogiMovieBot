import os, sys

PieceName_normal2kanji = {
    "OU" : "玉",
    "HI" : "飛",
    "KA" : "角",
    "KI" : "金",
    "GI" : "銀",
    "KE" : "桂",
    "KY" : "香",
    "FU" : "歩",
    "RY" : "龍",
    "UM" : "馬",
    "NG" : "成銀",
    "NK" : "成桂",
    "NY" : "成香",
    "TO" : "と"
}

PieceName_kanji2normal = {kanji : key for key, kanji in PieceName_normal2kanji.items()}

number2kanji = {
    1 : "一", 2: "二", 3 : "三", 4 : "四", 5 : "五", 6 : "六", 7 : "七", 8 : "八", 9 : "九"
}

kanji2number = {kanji : key for key, kanji in number2kanji.items()}

final_states = ["中断", "投了", "持将棋", "千日手", "詰み", "切れ負け", "反則勝ち", "反則負け"]


def kifu_wars2normal(data):
    
    lines = data.split("\n")
    hands_normal = []
    hands_str = []

    for i, line in enumerate(lines):
        chunks = line.split(" ")

        # 指し手かどうかを判断
        try:
            order = int(chunks[0])

        except:
            continue

        blocks = [l for l in line.split(" ") if l != ""]
        if  len(blocks) < 2:
            print(blocks)
            break

        hand = blocks[1]
        hand_str = hand.split("(")[0]

        if hand in final_states:
            break

        elif hand[-1] == "打":
            loc_from = PieceName_kanji2normal[hand[-2]]
            loc_to = str(int(hand[0])) + str(kanji2number[hand[1]])

        elif hand[0] == "同":
            loc_from = str(int(hand.split("(")[-1][:2]))
            loc_to = hands_normal[-1][2:4]  # 一つ前の手の移動先
            
            hand_str = "同" + hand_str.split("　")[-1]

        else:
            loc_from = str(int(hand.split("(")[-1][:2]))
            loc_to = str(int(hand[0])) + str(kanji2number[hand[1]])
            if hand.split("(")[0][-1] == "成":
                loc_to += "+"
                
        hand = loc_from + loc_to
        hands_normal.append(hand)
        hands_str.append(hand_str)
        
    return hands_normal, hands_str