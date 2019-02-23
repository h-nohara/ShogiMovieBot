// メッセージアクションをヒストリーに追加

$(document).on("click", "#AddAction", function(){

    SBoard.init_state_now();

    let text = $("#TextAction_text_box").val();
    let LightUp_pos_str = $("#" + "LightUpAction_buttons p").text();
    let Mark_pos_str = $("#" + "MarkAction_buttons p").text();

    let action = {"message" : {}, "board_state" : deepcopy_Board(SBoard.Board)};

    if ((text != null) && (text != "")){
        action["message"]["text"] = text;
    }
    if ((LightUp_pos_str != null) && (LightUp_pos_str != "")){
        action["message"]["light_up"] = LightUp_pos_str.split(",");
    }
    if ((Mark_pos_str != null) && (Mark_pos_str != "")){
        action["message"]["mark"] = Mark_pos_str.split(",");
    }


    History.add_action(action);
    show_message_contents(action);

})


// 手前に追加
$(document).on("click", "#AddActionBefore", function(){

    SBoard.init_state_now();

    let text = $("#TextAction_text_box").val();
    let LightUp_pos_str = $("#" + "LightUpAction_buttons p").text();
    let Mark_pos_str = $("#" + "MarkAction_buttons p").text();

    // 一個手前の盤面をコピー
    let order = History.watching_action["order_in_parent"];
    if (order > 0){
        var board_state_before = History.watching_action["parent"][order-1]["board_state"];
    }
    else {
        window.alert("シナリオの直後はだめ！（ただいま実装中）");
        return
    }

    // let action = {"message" : {}, "board_state" : deepcopy_Board(SBoard.Board)};
    let action = {"message" : {}, "board_state" : deepcopy_Board(board_state_before)};

    if ((text != null) && (text != "")){
        action["message"]["text"] = text;
    }
    if ((LightUp_pos_str != null) && (LightUp_pos_str != "")){
        action["message"]["light_up"] = LightUp_pos_str.split(",");
    }
    if ((Mark_pos_str != null) && (Mark_pos_str != "")){
        action["message"]["mark"] = Mark_pos_str.split(",");
    }


    History.add_action_before(action);
    show_message_contents(action);

})


// メッセージアクションの内容を更新

$(document).on("click", "#UpdateAction", function(){

    let action = History.watching_action;

    // 現在参照しているのがメッセージアクションかチェック
    if (Object.keys(action).indexOf("message") < 0){
        window.alert("メッセージアクションにのみ適用できます");
        exit;
    }

    let text = $("#TextAction_text_box").val();
    let LightUp_pos_str = $("#" + "LightUpAction_buttons p").text();
    let Mark_pos_str = $("#" + "MarkAction_buttons p").text();

    if ((text != null) && (text != "")){
        action["message"]["text"] = text;
    }
    else{
        delete action["message"]["text"];
    }

    if ((LightUp_pos_str != null) && (LightUp_pos_str != "")){
        action["message"]["light_up"] = LightUp_pos_str.split(",");
    }
    else{
        delete action["message"]["light_up"];
    }

    if ((Mark_pos_str != null) && (Mark_pos_str != "")){
        action["message"]["mark"] = Mark_pos_str.split(",");
    }
    else{
        delete action["message"]["mark"];
    }

    action["is_watching"] = true;
    History.update_view();
    show_message_contents(action);
    
})



// fly_toアクションを追加

$(document).on("click", "#add_FlyTo", function(){

    // 現在参照しているのがmessageだったらエラーを出す
    if (Object.keys(History.watching_action).indexOf("message") > 0){
        window.alert("メッセージのところにfly_toは追加できません");
        exit;
    }

    let action = {"fly_to" : null, "board_state" : deepcopy_Board(SBoard.Board)};
    History.add_action(action, true);
})



// アクションを削除
$(document).on("click", "#DelAction", function(){

    SBoard.init_state_now();

    let order = History.watching_action["order_in_parent"];

    // サブシナリオの最初を削除したら
    if (order == 0){

        // initialは削除できない
        if (Object.keys(History.watching_action).indexOf("move") >= 0){
            if (History.watching_action["move"] == "initial"){
                window.alert("最初は削除できません");
                exit;
            }
        }

        // 見ているもの以降を削除
        // History.watching_action["parent"].splice(order);
        History.watching_action["parent"] = [];

        History.history = handle_emp_scenario(History.history);

       // 画面更新
       History.update_view();
       show_message_contents(History.watching_action);
       SBoard.Board = deepcopy_Board(History.watching_action["board_state"]);
       SBoard.draw_main_board();

    }

    else{
        // 見ているものを更新
        History.watching_action = History.watching_action["parent"][order-1];
        History.watching_action["is_watching"] = true;

        // 見ているもの以降を削除
        History.watching_action["parent"].splice(order);
        
        // 画面更新
        History.update_view();
        show_message_contents(History.watching_action);
        SBoard.Board = deepcopy_Board(History.watching_action["board_state"]);
        SBoard.draw_main_board();
    }
    
})


// function handle_emp_scenario(history){

//     // ブランチを削除した時（ブランチの最初のアクションを削除した時）に、historyを編集

//     for (let i=0; i<history.length; i++){
//         let action = history[i];

//         // シナリオアクションを見つけたら
//         if (Object.keys(action).indexOf("scenarios") >= 0){
//             let emp_sc_number = null;
//             let n_sub_sc = action["scenarios"].length;

//             for (let j=0; j<n_sub_sc; j++){
//                 sub_sc = action["scenarios"][j];

//                 // 空のシナリオだったら
//                 if (sub_sc.length == 0){
//                     emp_sc_number = j;
//                     break;
//                 }
//                 // 空じゃなかったら、そのシナリオの中身を同じようにチェック
//                 else{
//                     action["scenarios"][j] = handle_emp_scenario(sub_sc);
//                 }
//             }
//             // 空のシナリオを見つけていたら
//             if (emp_sc_number != null){
//                 if (n_sub_sc >= 3){
//                     action["scenarios"].splice(emp_sc_number, 1);
//                 }
//                 else{
//                     let survive_sub_sc_number = Math.abs(action["selected_scenario"] - 1);  // 現在見ているのと別の方のシナリオ
//                     if (survive_sub_sc_number > 1){
//                         window.alert("koara");
//                         exit;
//                     }
//                     let tail_actions = action["scenarios"][survive_sub_sc_number];
//                     for (let tail_action of tail_actions){
//                         tail_action["parent"] = history;
//                     }

//                     history.splice(-1);  // ブランチアクションを削除（親の最後)
//                     history = history.concat(tail_actions); // 確認　見ていない方のサブシナリオを親の最後に加える

//                     History.watching_action = history[i-1];
//                     History.watching_action["is_watching"] = true;
//                 }
//             }
//         }
//     }

//     return history;
// }


function handle_emp_scenario(history){

    // ブランチを削除した時（ブランチの最初のアクションを削除した時）に、historyを編集

    for (let i=0; i<history.length; i++){
        let action = history[i];

        // シナリオアクションだったら
        if (Object.keys(action).indexOf("scenarios") >= 0){

            console.log("find scenarios");

            let n_sub_sc = action["scenarios"].length;
            console.log("n_sub : " + String(n_sub_sc));
            let selected_scenario = action["selected_scenario"];
            let watching_sub_scenario = action["scenarios"][selected_scenario];

            // 空じゃなかったら、そのシナリオの中身を同じようにチェック
            if (watching_sub_scenario.length >= 1){
                action["scenarios"][selected_scenario] = handle_emp_scenario(watching_sub_scenario);
            }
            // 空のシナリオだったら
            else{
                console.log("find emp scenario");
                // 分岐が３つ以上なら、見ている分岐を削除するだけ
                if (n_sub_sc >= 3){
                    console.log("n_sub_sc = 3");
                    action["scenarios"].splice(selected_scenario, 1);
                    action["selected_scenario"] = 0;
                }
                // 分岐が２つなら、分岐をなくして連結
                else if (n_sub_sc == 2){

                    console.log("n_sub_sc = 2");

                    action["scenarios"].splice(selected_scenario, 1);  // 今見ている方の分岐を削除

                    // 連結するアクションたち
                    let tail_actions = action["scenarios"][0];
                    for (let tail_action of tail_actions){
                        tail_action["parent"] = history;
                    }

                    history.splice(i, 1);  // 分岐アクション自体を削除
                    history = history.concat(tail_actions); // 見ていない方のサブシナリオを親の最後に加える

                    History.watching_action = history[i-1];
                    History.watching_action["is_watching"] = true;

                }
                // 分岐は２つ以上あるはず
                else {
                    window.alert("バグです。「分岐は１つだけのはず」と作成者に報告してください");
                }
            }
        }
    }

    console.log("this is result");
    console.log(history);

    return history;
}




// メッセージエフェクトを足すボタンを押した時
$(document).on("click", ".one_action_add_button", function(){
    SBoard.now_is_adding_action = !SBoard.now_is_adding_action;
    if (SBoard.now_is_adding_action){
        $(".OneSquare").css("background-color", "gold");
        show_effects(false);
        let adding_action_kind = this.id.split("_")[1];
        SBoard.now_is_adding_kind = adding_action_kind;
    }
    else{
        // $(".OneSquare").css("background-color", SBoard.default_color);
        show_effects();
    }
})


// メッセージエフェクトを消すボタンを押した時
$(document).on("click", ".one_action_reflesh_button", function(){
    let adding_action_kind = this.id.split("_")[1]; // "LightUp" or "Mark"
    $("#" + adding_action_kind + "Action_buttons" + " p").text("");
})

