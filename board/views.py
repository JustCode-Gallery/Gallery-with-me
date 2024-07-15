from django.shortcuts import render, redirect
from .models import Post
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import os
from .forms import PostForm
from django.utils import timezone
from exhibit.models import ArtExhibit
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject

User = get_user_model()



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
    user = request.user
    
    if request.method == 'POST':
        
        form = PostForm()
        uploaded_files = request.POST.get('uploadedFiles')

        if uploaded_files:
            uploaded_files = json.loads(uploaded_files)
            request.session['uploaded_files'] = uploaded_files

        return redirect('board:board_create_form')
    
    else:  # GET 요청 처리
        form = PostForm()

    context = {
        'form': form,
        'user':user,
    }
    return render(request, 'board/board_create_form.html', context)

# 게시하기 눌렀을 때 
def form_submit(request):
    if request.method == 'POST':
        # 폼 제출 시 Title / content / 전시 / user
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
             # request.user를 직접 사용하지 않고, User 모델 객체를 사용하여 처리
            try:
                user = User.objects.get(pk=request.user.pk)
                post.user = user
            except User.DoesNotExist:
                # 사용자 객체를 찾을 수 없는 경우에 대한 예외 처리
                # 특별한 처리가 필요하다면 여기에 구현
                pass

            post.post_timestamp = timezone.now()
            post.save()
           


            # post = Post.objects.create(
            #     post_title = post.post_title,
            #     post_content = post.post_content,
            #     post_timestamp = timezone.now(),
            #     user = post.user,
            #     exhibit = post.exhibit,
            # )
            # post.save()
        
            # post = form.save(commit=False)
            # post.user = request.user
            # post.post_timestamp = timezone.now()
            # post.save()

            # exhibit = ArtExhibit.objects.filter(id=id)

        
        
        # 성공적으로 저장되었을 때 세션에서 업로드된 파일 데이터 삭제
            if 'uploaded_files' in request.session:
                del request.session['uploaded_files']
            
            return redirect('board:board_list')
        else:
            # 폼이 유효하지 않은 경우 폼을 다시 렌더링하여 에러 메시지를 표시합니다.
            return render(request, 'board/board_create_form.html', {'form': form})

     # 유효하지 않은 폼 데이터가 있을 경우 다시 폼을 보여줌
    print("유효하지 않은 데이터")
    return redirect('board:board_create_form')

def board_detail(request):
    post = Post.objects.all()
    context = {
        'posts' : post
    }
    return render(request, 'board/board_detail.html', context)

def temp_upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        fs = FileSystemStorage(location=settings.TEMP_UPLOAD_DIR)
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)
        return JsonResponse({'file_url': file_url, 'filename': filename})
    return JsonResponse({'error': 'Invalid request'}, status=400)