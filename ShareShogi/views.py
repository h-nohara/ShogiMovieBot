
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def login_page(request):
    return render(request, "ShareShogi/loginShareShogi.html")

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

@login_required(login_url="/ShareShogi/accounts/loginpage")
def myBook_page(request):
    return render(request, "ShareShogi/myBooks.html")

@login_required(login_url="/ShareShogi/accounts/loginpage")
def newBook_page(request):
    return render(request, "ShareShogi/newBook.html")

@login_required(login_url="/ShareShogi/accounts/loginpage")
def bookEditor_page(request):
    return render(request, "ShareShogi/bookEditor.html")

@login_required(login_url="/ShareShogi/accounts/loginpage")
def myChapters_page(request):
    return render(request, "ShareShogi/myChapters.html")

@login_required(login_url="/ShareShogi/accounts/loginpage")
def newChapter_page(request):
    return render(request, "ShareShogi/newChapter.html")

@login_required(login_url="/ShareShogi/accounts/loginpage")
def newScene_page(request):
    return render(request, "ShareShogi/newScene.html")

@login_required(login_url="/ShareShogi/accounts/loginpage")
def myScenes_page(request):
    return render(request, "ShareShogi/myScenes.html")

@login_required(login_url="/ShareShogi/accounts/loginpage")
def testUpload_page(request):
    return render(request, "ShareShogi/test_jqueryUpload.html")

@login_required(login_url="/ShareShogi/accounts/loginpage")
def newAccountForAdmin_page(request):
    return render(request, "ShareShogi/newAccountForAdmin.html")

