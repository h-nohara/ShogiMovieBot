from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/account/login")
def board_page(request):
    return render(request, "board/gui.html")

@login_required(login_url="/account/login")
def initial_board_page(request):
    return render(request, "board/initial_board_editor.html")

@login_required(login_url="/account/login")
def board_test_page(request):
    return render(request, "board/board_editor.html")