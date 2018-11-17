# {"history" : [{}, {}, ...]}という形式でやり取り


def modify_one_action(action):

    '''
    jsonでデータを受け取った時に、成りを表す"+"が空文字になってしなうのを修正
    "move"と"legal_moves"
    '''

    if "move" in action.keys():
        if len(action["move"]) == 5:
            action["move"] = action["move"][:4] + "+"

    for i, move in enumerate(action["board_state"]["legal_moves"]):
        if (len(move) == 5) and (move[-1] != "+"):
            action["board_state"]["legal_moves"][i] = move[:4] + "+"

    return action


def modify(history):

    modified_history = []

    for action in history:

        # ブランチだったら
        if "scenarios" in action.keys():
            for i, sc in enumerate(action["scenarios"]):
                action["scenarios"][i] = modify(sc)
                
        modified_history.append(modify_one_action(action))

    return modified_history