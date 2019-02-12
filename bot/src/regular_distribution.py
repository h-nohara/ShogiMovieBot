import os, sys, glob2, json, pytz
import datetime, random
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.user import User
from accounts.models.project import Project
from bot.models.scenario import Scenario
from bot.models.message import Message
from bot.models.subscription import Subscription

# api
from bot.src.line_bot_api import line_bot_api, push_text_message, nohara_first_id
from bot.src.distribute_now import distribute


# 定期配信

@csrf_exempt
def regular_distribution_request(request):

    regular_distribution()

    return JsonResponse({"code" : 200})

@csrf_exempt
def test_regular_distribution_request(request):

    print("ーーテスト配信を開始します")

    push_text_message(text="ーーテスト配信を開始します", line_id=nohara_first_id)

    distribute_random(is_test=True)

    push_text_message(text="ーーテスト配信終了", line_id=nohara_first_id)

    print("ーーテスト配信終了")

    return JsonResponse({"code" : 200})


def regular_distribution():

    # 貯まったキューを捌く
    # process_queue(reader=None, kind="random")  # とりあえずランダム配信のみ

    # ランダム購読設定者に配信
    distribute_random(reader=None)

    print("all finished : 定期配信")
    

        


# def process_queue(reader=None, kind=None):

#     '''
#     シナリオ配信のキューを処理する

#     reader : Userオブジェクト。このユーザが購読しているキューのみを処理。Noneなら全ユーザを対象にする。
#     kind : この種類の配信のみを処理。Noneなら全ての種類を対象にする。["random"]
#     '''

#     # 今日の日付
#     now = datetime.datetime.now()
#     date_today = now.date()

#     # キューを取得

#     if reader is None:
#         record_list_DistributionQueue = DistributionQueue.objects.all()

#     else:
#         record_list_DistributionQueue = [DistributionQueue.objects.get(reader=reader)]

#     # キューを処理
    
#     for record_DistributionQueue in record_list_DistributionQueue:

#         # 購読の種類を照らし合わせる
#         if kind is not None:
#             if record_DistributionQueue.kind != kind:
#                 continue

#         date_distribution = record_DistributionQueue.date_distribution

#         # 配信日が今日の場合、配信する
#         if date_today == date_distribution.date():

#             user_id = record_DistributionQueue.reader.id
#             scenario_id = record_DistributionQueue.scenario.id
#             distribute(scenario_id=scenario_id, user_id=user_id)

#     print("all finished : キューのシナリオの配信")


def distribute_random(reader=None, is_test=False):

    '''
    ランダム購読設定をしているユーザにシナリオを配信する。
    購読に設定している、自作のシナリオと他人のシナリオ、またはどちらかからランダムでシナリオを選んで配信。

    reader : Userオブジェクト。このユーザが購読するシナリオのみを対象にする。Noneなら全ユーザを対象にする。
    us_test : Trueなら、次回配信日を更新しない。
    '''

    # 購読者を取得
    if is_test:
        me = User.objects.get(username="nohara")
        record_list_User = [me]
    else:
        if reader is None:
            record_list_User = User.objects.all()
        else:
            record_list_User = [reader]

    # 今日の日付
    jp = pytz.timezone('Asia/Tokyo')

    now = datetime.datetime.now()
    now = now.astimezone(jp)  # 日本時間に

    # 購読者ごとに配信

    for record_User in record_list_User:

        # 配信設定を確認

        is_enabled_RandomSubscription_own_scenario = record_User.is_enabled_RandomSubscription_own_scenario
        is_enabled_RandomSubscription_others_scenario = record_User.is_enabled_RandomSubscription_others_scenario

        if (not is_enabled_RandomSubscription_own_scenario) and (not is_enabled_RandomSubscription_others_scenario):
            continue

        next_date_RandomSubscription = record_User.next_date_RandomSubscription
        if next_date_RandomSubscription is None:
            continue
        else:
            next_date_RandomSubscription = next_date_RandomSubscription.astimezone(jp)  # 日本時間に

        # 配信日だったら
        if now.date() == next_date_RandomSubscription.date():

            # 次回配信日を更新
            if not is_test:
                next_date = now + datetime.timedelta(days=record_User.interval_RandomSubscription)
                record_User.next_date_RandomSubscription = next_date
                record_User.save()


            # シナリオ一覧を取得する

            subscriptions = []
            # scenarios_priority = []

            # 自作のシナリオ
            if is_enabled_RandomSubscription_own_scenario:

                record_list_Scenario = Subscription.objects.filter(reader=record_User, author=record_User, kind="random", is_enabled=True)
                subscriptions.extend(list(record_list_Scenario))

            # 他人のシナリオ
            if is_enabled_RandomSubscription_others_scenario:

                record_list_Scenario = Subscription.objects.filter(reader=record_User, kind="random", is_enabled=True).exclude(author=record_User).filter(is_scenario_public=True)
                subscriptions.extend(list(record_list_Scenario))


            # 配信
            push_text_message(text="＊＊ランダム購読の配信です＊＊", line_id=record_User.line_id)

            if len(subscriptions) > 0:
                # ランダムに選択
                choiced = random.choice(subscriptions)
                scenario_id = choiced.scenario.id
                distribute(scenario_id=int(scenario_id), user_id=int(record_User.id))

    print("all finished : ランダム購読配信")