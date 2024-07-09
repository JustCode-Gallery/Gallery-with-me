from django.shortcuts import render
from .models import Post

# Create your views here.
def board_list(request):
    post = Post.objects.all()
    context = {
        'posts' : post
    }
    return render(request, 'board/board_list.html', context)