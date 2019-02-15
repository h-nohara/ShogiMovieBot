import os, sys, glob2, json
from ShogiMovieBot.settings import BASE_DIR

from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# db
from accounts.models.project import Project
from accounts.models.info import Info
from bot.models.scenario import Scenario
from bot.models.message import Message
from bot.models.subscription import Subscription


@csrf_exempt
def delete_scenario_request(request):

    # receive
    print(request.POST)
    data = json.loads(request.body.decode("utf-8"))
    scenario_id = data["scenario_id"]
    scenario_id = int(scenario_id)

    # delete
    delete_scenario(scenario_id)

    return JsonResponse({"code" : 200})


def delete_scenario(scenario_id):

    record_Scenario = Scenario.objects.get(id=scenario_id)
    scenario_title = record_Scenario.title

    # メッセージを削除
    record_list_Message = Message.objects.filter(scenario=record_Scenario)
    for record_Message in record_list_Message:
        record_Message.delete()

    # 購読から削除
    record_list_Subscription = Subscription.objects.filter(scenario=record_Scenario)

    for record_Subscription in record_list_Subscription:

        # シナリオが削除されたことを、購読者に通知
        reader = record_Subscription.reader
        record_Info = Info(
            user = reader,
            message = "{}は作成者によって削除されました".format(scenario_title)
        )
        record_Info.save()

        record_Subscription.delete()

    record_Scenario.delete()  # レコード削除