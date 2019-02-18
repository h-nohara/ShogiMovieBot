import os, sys
import json

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User



@login_required
def get_account_info_request(request):

    record_User = request.user

    username = record_User.username
    nickname = record_User.nickname
    is_enabled_RandomSubscription_own_scenario = record_User.is_enabled_RandomSubscription_own_scenario
    is_enabled_RandomSubscription_others_scenario = record_User.is_enabled_RandomSubscription_others_scenario
    interval_RandomSubscription = record_User.interval_RandomSubscription
    next_date_RandomSubscription =record_User.next_date_RandomSubscription

    info = {
        "username" : username,
        "nickname" : nickname,
        "is_enabled_RandomSubscription_own_scenario" : is_enabled_RandomSubscription_own_scenario,
        "is_enabled_RandomSubscription_others_scenario" : is_enabled_RandomSubscription_others_scenario,
        "interval_RandomSubscription" : interval_RandomSubscription,
        "next_date_RandomSubscription" : next_date_RandomSubscription
    }

    result = {
        "code" : 200,
        "data" : {
            "info" : info
        }
    }

    return JsonResponse(result)

