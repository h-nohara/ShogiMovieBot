from django.shortcuts import render, redirect


def project_scenarios_page(request):
    return render(request, "bot/project_scenarios.html")

def scenario_editor_page(request):
    return render(request, "bot/scenario_editor.html")