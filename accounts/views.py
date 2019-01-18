from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def login_page(request):
    return render(request, "accounts/login.html")

@login_required(login_url="/account/login")
def home_page(request):
    return render(request, "accounts/home.html")

def new_account_page(request):
    return render(request, "accounts/new_account.html")