import os, sys, glob2, json, datetime
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.user import User
from accounts.models.project import Project
from bot.models.scenario import Scenario
from bot.models.message import Message
from bot.models.subscription import Subscription


@csrf_exempt
def change_subscription_setting_request(request):

    '''
    シナリオの購読設定を変更
    '''

    print(request.POST)
    payload = json.loads(request.body.decode("utf-8"))

    scenario_id = payload["scenario_id"]
    is_subsc = payload["is_subscribing"]

    scenario_id = int(scenario_id)

    record_Scenario = Scenario.objects.get(id=scenario_id)
    record_User = request.user
    if not record_User.is_authenticated():
        print("!!!!!!!! not logged in")
        return JsonResponse({"code" : 400})

    record_list_Subscription = Subscription.objects.filter(scenario=record_Scenario, reader=record_User)
    n = len(record_list_Subscription)

    # すでに購読したことがあったら、値を変更
    if n == 1:
        record_Subscription = record_list_Subscription[0]
        record_Subscription.is_enabled = is_subsc

    # 初の購読だったら、データベースに新規登録
    elif n == 0:
        record_Subscription = Subscription(
            reader = record_User,
            scenario = record_Scenario,
            author = record_Scenario.project.user,
            is_scenario_public = record_Scenario.is_public,
            is_enabled = True,
            kind = "random"
        )
        record_Subscription.save()

    else:
        print("複数登録されています！")
    

    # 次回のランダム配信日のチェック
    now = datetime.datetime.now()
    next_date = record_User.next_date_RandomSubscription
    # もし次回配信日が古かったら、更新
    if is_subsc:
        if (next_date is None) or (now > next_date):
            record_User.next_date_RandomSubscription = now + datetime.timedelta(days=record_User.interval_RandomSubscription)
            record_User.save()

    result = {
        "code" : 200,
    }

    return JsonResponse(result)