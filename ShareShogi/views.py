
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def search_page(request):
    return render(request, "ShareShogi/search_book.html")

def chapters_page(request):
    return render(request, "ShareShogi/chapters.html")

def scene_page(request):
    return render(request, "ShareShogi/scenes.html")

def scene_demopage1(request):
    return render(request, "ShareShogi/scenes-demo1.html")

def account_page(request):
    return render(request, "ShareShogi/account.html")

@login_required(login_url="/account/login")
def myBook_page(request):
    return render(request, "ShareShogi/myBooks.html")

@login_required(login_url="/account/login")
def newBook_page(request):
    return render(request, "ShareShogi/newBook.html")

@login_required(login_url="/account/login")
def bookEditor_page(request):
    return render(request, "ShareShogi/bookEditor.html")

@login_required(login_url="/account/login")
def myChapters_page(request):
    return render(request, "ShareShogi/myChapters.html")

@login_required(login_url="/account/login")
def newChapter_page(request):
    return render(request, "ShareShogi/newChapter.html")

@login_required(login_url="/account/login")
def newScene_page(request):
    return render(request, "ShareShogi/newScene.html")

@login_required(login_url="/account/login")
def myScenes_page(request):
    return render(request, "ShareShogi/myScenes_test.html")