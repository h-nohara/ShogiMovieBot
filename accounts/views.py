from django.shortcuts import render, redirect


def login_page(request):
    return render(request, "accounts/login.html")

def home_page(request):
    return render(request, "accounts/home.html")

def new_account_page(request):
    return render(request, "accounts/new_account.html")