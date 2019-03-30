
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def search_page(request):
    return render(request, "ShareShogi/search_book.html")

def chapters_page(request):
    return render(request, "ShareShogi/chapter.html")

def scene_page(request):
    return render(request, "ShareShogi/scene.html")

def account_page(request):
    return render(request, "ShareShogi/account.html")