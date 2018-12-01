

// todo loadした時にparentを設定し直す

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