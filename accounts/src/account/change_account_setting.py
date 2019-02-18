import os, sys
import json

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User



@login_required
@csrf_exempt
def change_account_setting_request(request):

    user_id = int(request.user.id)
    record_User = User.objects.get(id=user_id)

    data = json.loads(request.body.decode("utf-8"))

    # username = data["username"]
    nickname = data["nickname"]
    # is_enabled_RandomSubscription_own_scenario = data["is_enabled_RandomSubscription_own_scenario"]
    # is_enabled_RandomSubscription_others_scenario = data["is_enabled_RandomSubscription_others_scenario"]
    # interval_RandomSubscription = data["interval_RandomSubscription"]
    # next_date_RandomSubscription = data["next_date_RandomSubscription"]

    # record_User.username = username
    record_User.nickname = nickname
    # record_User.is_enabled_RandomSubscription_own_scenario = is_enabled_RandomSubscription_own_scenario
    # record_User.is_enabled_RandomSubscription_others_scenario = is_enabled_RandomSubscription_others_scenario
    # record_User.interval_RandomSubscription = interval_RandomSubscription
    # record_User.next_date_RandomSubscription = next_date_RandomSubscription

    record_User.save()

    print("ニックネーム : {}".format(nickname))
    print("ニックネーム保存 : {}".format(record_User.nickname))

    return JsonResponse({"code" : 200})

