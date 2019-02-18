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
