import os, sys, json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/account/login")
@csrf_exempt
def project_scenarios_page(request):

    data = json.loads(request.body.decode("utf-8"))
    project_id = data["project_id"]
    project_id = int(project_id)

    request.session.project_id = project_id

    return render(request, "bot/project_scenarios.html")


@login_required(login_url="/account/login")
@csrf_exempt
def scenario_editor_page(request):

    data = json.loads(request.body.decode("utf-8"))
    scenario_id = data["scenario_id"]
    scenario_id = int(scenario_id)

    request.session.scenario_id = scenario_id

    return render(request, "bot/scenario_editor.html")



@login_required(login_url="/account/login")
@csrf_exempt
def public_scenarios_page(request):
    return render(request, "bot/public_scenarios.html")