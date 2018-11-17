

// todo loadした時にparentを設定し直す

// 動画生成
$(document).on("click", "#finish", function(){

    console.log("start make movie");

    let new_history = [];
    let history_copy = copy_history_without_parent(History.history, new_history);

    // コピーした時にオリジナルhistoryのparentが削除されてしまったので、再設定
    set_parent(History.history);

    $.ajax({
        url : "/make_movie",
        type : "POST",
        data: JSON.stringify({"history" : history_copy}),
        timeout: 1000 * 600
    })
    .done(function(no_data){
        console.log("pushed to python make image");
        window.alert("動画を生成しました");
    })
    .fail(function(jqXHR, textStatus, errorThrown){
        console.log("oh my image");
    })
})




function copy_history_without_parent(history, new_history){

    for (let action of history){
        delete action["parent"];

        if (Object.keys(action).indexOf("scenarios") >= 0){
            for (let i = 0; i<action["scenarios"].length; i++){
                let mini_sc = action["scenarios"][i];
                let the_new = [];
                action["scenarios"][i] = copy_history_without_parent(mini_sc, the_new);
            }
        }

        let action_copy = $.extend(true, {}, action);
        new_history.push(action_copy);
    }

    return new_history;
}


function set_parent(history){

    for (let action of history){

        action["parent"] = history;

        if (Object.keys(action).indexOf("scenarios") >= 0){
            for (let mini_sc of action["scenarios"]){
                set_parent(mini_sc);
            }
        }
    }
}