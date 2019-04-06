import os, sys, json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# db
from accounts.models.user import User
from ShareShogi.models.book import Book
from ShareShogi.models.chapter import Chapter
from ShareShogi.models.scene import Scene
from ShareShogi.models.opening import Opening

# src


@csrf_exempt
def get_openings_request(request):

    '''
    特定の戦型に紐ずく戦型を全て取得
    '''

    if request.method == "POST":
        payload = request.POST

    else:
        raise("only POST accept")

    opening_sente = payload["opening_sente"]
    opening_gote = payload["opening_gote"]


    # openingの情報を取得する
    opening_list_sente = get_openings(opening_sente)
    opening_list_gote = get_openings(opening_gote)

    result = {
        "code" : 200,
        "result": {
            "sente" : opening_list_sente,
            "gote" : opening_list_gote
        }
    }
    
    return JsonResponse(result)



def get_opening_tree(opening, is_get_listed=False):

    '''
    opening : str or record
    is_get_listed : Falseならツリーを取得、Trueならリストを取得
    '''

    if type(opening) == str:
        record_Opening = Opening.objects.get(name=opening)

    # 子一覧を取得
    queryset_Openings = Opening.objects.filter(parent=record_Opening)

    if not is_get_listed:

        opening_tree = {
            "name" : record_Opening.name,
            "childs" : None
        }

        opening_tree["childs"] = [get_opening_tree(child_opening, is_get_listed=False) for child_opening in queryset_Openings]

        return opening_tree

    else:

        all_opening_list = [record_Opening]

        for child_opening in queryset_Openings:
            openings = get_opening_tree(record_Opening, is_get_listed=True)
            return openings
        # all_opening_list += [get_opening_tree(child_opening, is_get_listed=True).name for child_opening in queryset_Openings]

        return all_opening_list



