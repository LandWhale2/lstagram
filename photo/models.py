from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse



class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user') #ForeignKey 를 사용해서 User 테이블과 관계를만듦. User? 장고에서 기본적으로 사용하는 사용자모델 ondelete 는 모델 삭제시 값을 어떻게할것이냐의것
    text = models.TextField(blank=True) #text 필드 문자열 길이 제한 x
    image = models.ImageField(upload_to = 'timeline_photo/%Y/%m/%d') #알아서 등록날짜랑 등록일 처리
    created = models.DateTimeField(auto_now_add = True) #글을 작성할때 시간을 가지고 경로에 맞게끔 값을 넣어줌
    updated = models.DateTimeField(auto_now = True) #글 수정일을 저장하기위한 날짜 필드 ,, 객체가 수정될때마다 자동으로 값을 설정해준다

    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    favorite = models.ManyToManyField(User, related_name='favorite_post', blank=True)

    def __str__(self):
        return "text : "+self.text 


    class Meta:
        ordering = ['-created'] #ordering 변수는 객체들을 어떤기준으로 정렬할것인지 설정하는옵션

    def get_absolute_url(self):
        return reverse('photo:detail', args=[self.id]) #상세페이지로 이동하도록 absolute url 설정 이후에 views에서 return super가 나오면 자동적으로 실행