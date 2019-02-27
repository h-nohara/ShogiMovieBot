from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def login_page(request):
    return render(request, "accounts/login.html")

@login_required(login_url="/account/login")
def home_page(request):
    return render(request, "accounts/home.html")


@login_required(login_url="/account/login")
def new_account_page(request):
    return render(request, "accounts/new_account.html")


# sp

@login_required(login_url="/account/login")
def home_page_sp(request):
    return render(request, "accounts/sp/home.html")



# テスト

@login_required(login_url="/account/login")
def test_home_page_sm(request):
    return render(request, "accounts/sp/home.html")


@login_required(login_url="/account/login")
def home_page_future(request):
    return render(request, "accounts/home_future.html")