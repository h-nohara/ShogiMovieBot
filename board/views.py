from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/account/login")
def board_page(request):
    return render(request, "board/board_editor.html")

@login_required(login_url="/account/login")
def initial_board_page(request):
    return render(request, "board/initial_board_editor.html")

# sp

@login_required(login_url="/account/login")
def board_page_sp(request):
    return render(request, "board/sp/board_editor_sm.html")

@login_required(login_url="/account/login")
def initial_board_page_sp(request):
    return render(request, "board/sp/initial_board_editor_sm.html")


# テストページ

@login_required(login_url="/account/login")
def test_board_page_sm(request):
    return render(request, "board/sp/board_editor_sm_nonButton.html")

@login_required(login_url="/account/login")
def test_initial_board_page_sm(request):
    return render(request, "board/sp/initial_board_editor_sm.html")