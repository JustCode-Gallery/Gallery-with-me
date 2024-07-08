from django.shortcuts import render

# Create your views here.
def board_list(request):
    return render(request, 'board/board_list.html')