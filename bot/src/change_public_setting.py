import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.project import Project
from bot.models.scenario import Scenario
from bot.models.message import Message
from bot.models.subscription import Subscription


@csrf_exempt
def change_public_setting_request(request):

    '''
    シナリオの公開設定を変更
    '''

    print(request.POST)
    payload = json.loads(request.body.decode("utf-8"))
    # scenario_id = payload["scenario_id"]
    # scenario_id = int(scenario_id)
    is_public = payload["is_public"]

    scenario_id = int(request.session.get("scenario_id"))

    # シナリオの公開設定を更新
    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_Scenario.is_public = is_public
    record_Scenario.save()

    # 購読レコードのシナリオ公開情報を更新
    for record_Subscription in Subscription.objects.filter(scenario=record_Scenario):
        record_Subscription.is_scenario_public = is_public
        record_Subscription.save()

    result = {
        "code" : 200,
    }

    return JsonResponse(result)