from django.shortcuts import render, redirect
from .models import Post, PostImage
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import os
from .forms import PostForm, PostSearchForm
from django.utils import timezone
from exhibit.models import ArtExhibit
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

User = get_user_model()



# Create your views here.
def board_list(request):
    post = Post.objects.all().order_by('-post_timestamp')  # 최신 포스트가 먼저 나오도록 정렬
    
    # 페이지네이션
    paginator = Paginator(post, 12)  # 한 페이지에 10개씩 보이도록 설정
    page_number = request.GET.get('page', 1)  # 기본적으로 첫 페이지를 설정
    page_obj = paginator.get_page(page_number)

    post_img = PostImage.objects.filter(image_order=0)
    search_form = PostSearchForm()
    user = request.user


    context = {
        'posts' : page_obj, # 페이지네이션 된 포스트
        'post_img': post_img,
        'search_form': search_form,
        'user':user,
        'paginator': paginator,
        'page_obj': page_obj,
    }

    return render(request, 'board/board_list.html', context)

@login_required
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
            

            exhibit_title = form.cleaned_data.get('exhibit')
            try:
                exhibit = ArtExhibit.objects.get(title=exhibit_title)
                post.exhibit = exhibit
            except ArtExhibit.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': '지정된 전시가 없습니다.'}, status=400)
            # post.exhibit = form.cleaned_data['exhibit']  # 올바른 Exhibit 인스턴스를 설정

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
            # del request.session['uploaded_files']
            print("세션에서 'uploaded_files' 삭제됨")
                # 현재 세션 데이터 출력 (디버깅용)
            print("현재 세션 데이터:", request.session.items())
            
            return JsonResponse({'status':'success', 'pk': post.id})
        else:
            # 폼이 유효하지 않은 경우 폼을 다시 렌더링하여 에러 메시지를 표시합니다.
            # return render(request, 'board/board_create_form.html', {'form': form})
        # 폼이 유효하지 않은 경우 JSON 응답을 반환
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

     # 유효하지 않은 폼 데이터가 있을 경우 다시 폼을 보여줌
    print("유효하지 않은 데이터")
    # return redirect('board:board_create_form')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def board_detail(request, pk):
    post = Post.objects.get(pk=pk)
    post_img = PostImage.objects.filter(post=post)
    user = request.user
    post.visitors += 1
    post.save()
    
    context = {
        'post' : post,
        'post_img': post_img,
        'user': user,
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

def board_search(request):

    context = {
        'search_form': PostSearchForm(),
    }

    if request.method=="POST":
        search_form = PostSearchForm(request.POST)
        if search_form.is_valid():
            searchWord = search_form.cleaned_data['search_word']
            post_list = Post.objects.filter(
                Q(post_title__icontains=searchWord) | 
                Q(post_content__icontains=searchWord)
            ).distinct()    # 기본정렬순서 db최신순
            # ).order_by('').distinct() 정렬 순서 직접지정

            context.update({
                'search_term': searchWord,
                'object_list': post_list,
            })
        else:
            context.update({
                'search_form': search_form,
                'form_errors': search_form.errors
            })
    
    return render(request, 'board/board_search.html', context)

# 전시검색 자동완성 
def exhibit_autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term', '')
        # term을 사용하여 제목에 term이 포함된 전시를 필터링
        exhibits = ArtExhibit.objects.filter(title__icontains=term)
        results = [{'id': exhibit.id, 'title': exhibit.title} for exhibit in exhibits]
        return JsonResponse(results, safe=False)


