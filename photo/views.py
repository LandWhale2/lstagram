from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Photo

class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list' #메인에서 보여줄 로직

class PhotoCreate(CreateView):
    model = Photo
    fields = ['author', 'text', 'image']
    template_name_suffix = '_create'
    success_url = '/'
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form' : form})


class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['author', 'text', 'image']
    template_name_suffix = '_update'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):#dispatch 보안상 권한 문제를 해결하기 위함.
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
            #삭제 페이지에서 권한이 없다 라고 띄우거나
            #detail 페이지로 들어가서 삭제에 실패했습니다 라고 띄우거나
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)


from django.http import HttpResponseRedirect
from django.contrib import messages


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete' 
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):#dispatch 보안상 권한 문제를 해결하기 위함.
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
            #삭제 페이지에서 권한이 없다 라고 띄우거나
            #detail 페이지로 들어가서 삭제에 실패했습니다 라고 띄우거나
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)


class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'
    

from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse

class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated: #로그인검사
            return HttpResponseForbidden() #거부
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id) #photo에 photo id 넣어줌
                user = request.user
                if user in photo.like.all(): #만약 이미 좋아요가 눌러져있으면 제거함.
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path= urlparse(referer_url).path
            return HttpResponseRedirect(path) #메인페이지에 위치해있다면 그 메인페이지에 있게하고 상세페이지에서 좋아요를 누르면 그 상세페이지로 redirect

class PhotoFavorite(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:    #로그인확인
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.favorite.all():
                    photo.favorite.remove(user)
                else:
                    photo.favorite.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)



class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self,request,*args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인 후 이용가능합니다.')
            return HttpResponseRedirect('/')
        return super(PhotoLikeList,self).dispatch(request,*args,**kwargs)
    
    def get_queryset(self):
        #내가 좋아요한 글 보여주기
        user = self.request.user
        queryset = user.like_post.all()
        return queryset

class PhotoFavoriteList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self,request,*args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인 후 이용가능합니다.')
            return HttpResponseRedirect('/')
        return super(PhotoFavoriteList,self).dispatch(request,*args,**kwargs)
    
    def get_queryset(self):
        #내가 저장한글 보여주기
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset

from django.shortcuts import render
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        #입력받은 내용을 이용해서 회원의 객체를 생성함
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        #회원 객체 생성하기
        user = User()
        user.username = username
        user.set_password(password)
        user.save()

        return render(request, 'accounts/signup_complete.html')
    
    else:
        #from 객체를 만들어서 전달
        context_values = {'form': 'this is form'}
        return render(request, 'accounts/signup.html', context_values)

