from django.shortcuts import render
from .models import Post

# Create your views here.
def board_list(request):
    post = Post.objects.all()
    context = {
        'posts' : post
    }
    return render(request, 'board/board_list.html', context)

def board_create(request):
    return render(request, 'board/board_create.html')

def  board_create_form(request):
    return render(request, 'board/board_create_form.html')

def board_detail(request):
    return render(request, 'board/board_detail.html')

