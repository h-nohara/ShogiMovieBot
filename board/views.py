from django.shortcuts import render


def board_page(request):

    return render(request, "board/gui.html")