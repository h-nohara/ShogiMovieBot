import os, sys, json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/account/login")
def project_scenarios_page(request):
    return render(request, "bot/project_scenarios.html")


@login_required(login_url="/account/login")
def scenario_editor_page(request):
    return render(request, "bot/scenario_editor.html")



@login_required(login_url="/account/login")
def public_scenarios_page(request):
    return render(request, "bot/public_scenarios.html")


@login_required(login_url="/account/login")
def subscribing_scenarios_page(request):
    return render(request, "bot/subscribing_scenarios.html")



# テストページ

@login_required(login_url="/account/login")
def test_project_scenarios_page_sm(request):
    return render(request, "bot/sm/project_scenarios.html")


@login_required(login_url="/account/login")
def test_scenario_editor_page_sm(request):
    return render(request, "bot/sm/scenario_editor.html")



@login_required(login_url="/account/login")
def test_public_scenarios_page_sm(request):
    return render(request, "bot/sm/public_scenarios.html")


@login_required(login_url="/account/login")
def test_subscribing_scenarios_page_sm(request):
    return render(request, "bot/sm/subscribing_scenarios.html")
