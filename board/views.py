from django.shortcuts import render, redirect
from .models import Post, PostImage
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import os
from .forms import PostForm
from django.utils import timezone
from exhibit.models import ArtExhibit
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.http import HttpResponse

User = get_user_model()



# Create your views here.
def board_list(request):
    post = Post.objects.all()
    post_img = PostImage.objects.filter(image_order=0)
    context = {
        'posts' : post,
        'post_img': post_img
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
                raise Exception('User 객체가 아닙니다.')

            post.post_timestamp = timezone.now()
            post.save()

            # 세션 / 서버 temp에서 파일 가져와야됨
            # 연결 hidden 으로 저장 시키든가 다른방법
            
            # 세션에서 업로드된 파일 정보 가져오기
            uploaded_files = request.session.get('uploaded_files', [])
            for index, file_info in enumerate(uploaded_files):
                if 'file_url' in file_info:
                    # 파일 절대 경로 구성
                    file_path = os.path.join(settings.TEMP_UPLOAD_DIR, file_info['filename'])
                    with open(file_path, 'rb') as file:
                        image = file.read()
                    
                    # 파일명에서 확장자 추출
                    _, ext = os.path.splitext(file_info['filename'])
                    ext = ext.lower()

                     # Django의 InMemoryUploadedFile으로 변환
                    memory_file = BytesIO(image)
                    memory_file.name = file_info['filename']
                    memory_file.seek(0)

                    post_img = PostImage.objects.create(
                        # image_url= image,
                        image_order=index,
                        post=post
                    )
                    
                    post_img.image_url.save(file_info['filename'], InMemoryUploadedFile(memory_file, None, file_info['filename'], 'image/%s' % ext.lower(), memory_file.tell, None))
                    
                    post_img.save()
                    
                    if os.path.exists(file_path):
                        os.remove(file_path)
                else:
                    # 'file_url' 키가 없을 경우 처리
                    print(f"'file_url'이 누락된 업로드 파일 정보: {file_info}")
              
        
            # 성공적으로 저장되었을 때 세션에서 업로드된 파일 데이터 삭제
            del request.session['uploaded_files']
            print("세션에서 'uploaded_files' 삭제됨")
           
                # 현재 세션 데이터 출력 (디버깅용)
            print("현재 세션 데이터:", request.session.items())
            
            return JsonResponse({'status':'success', 'pk': post.id})
        else:
            # 폼이 유효하지 않은 경우 폼을 다시 렌더링하여 에러 메시지를 표시합니다.
            return render(request, 'board/board_create_form.html', {'form': form})

     # 유효하지 않은 폼 데이터가 있을 경우 다시 폼을 보여줌
    print("유효하지 않은 데이터")
    return redirect('board:board_create_form')

def board_detail(request, pk):
    post = Post.objects.get(pk=pk)
    post_img = PostImage.objects.filter(post=post)
    # 저장된
    context = {
        'post' : post,
        'post_img': post_img,
    }
    return render(request, 'board/board_detail.html', context)

def temp_upload(request):
    # 브라우저에서 30초동안 신호를 받지 않을 때 서버 media폴더 tempd폴더에만 사진저장됨
    # 같은 유저인지 확인
    if request.method == 'POST':
        file = request.FILES['file']
        fs = FileSystemStorage(location=settings.TEMP_UPLOAD_DIR)
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)


         # 세션에 업로드된 파일 정보 저장
        user = User.objects.get(pk=request.user.pk)
        uploaded_files = request.session.get('uploaded_files', [])
        
        uploaded_files.append({'file_url': file_url, 'filename': filename, 'user': user.username })
        request.session['uploaded_files'] = uploaded_files
        
        # 테스트용 세션데이터 많아짐 > 임시 전체장고세션 비우기
        # del request.session['uploaded_files']

        return JsonResponse({'file_url': file_url, 'filename': filename})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# 세션 지우기
def refresh_session(request):
    if request.method == 'GET':
        # 세션에서 업로드된 파일 정보 가져오기
        del request.session['uploaded_files']
        return JsonResponse({'status': 'success'})
        
    return JsonResponse({'status': 'error'}, status=400)

def board_detail_edit(request,pk):
    post = Post.objects.get(pk=pk)
    post_img = PostImage.objects.filter(post=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid:
            form.save()
            return redirect('board:board_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'post': post,
        'form': form,
        'post_img': post_img,

    }

    return render(request,'board/board_detail_edit.html', context)

def board_delete(request, pk):
    if request.method=="POST":
        post = Post.objects.get(pk=pk)
        post.delete()

        return redirect('board:board_list')
    return HttpResponse(status=405)

def board_update(request, pk):
    if request.method=="POST":
        post = Post.objects.get(pk=pk)

        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect('board:board_detail', pk=pk)
    form = PostForm(instance=post)
    return HttpResponse(status=405)