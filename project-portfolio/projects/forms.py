from django import forms
from .models import Project, Rating
from django.contrib.auth.forms import UserCreationForm
from .models import User

# 사용자 회원가입 폼 클래스 (Django의 기본 UserCreationForm을 상속)
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User  # 사용자 모델을 기반으로 생성
        fields = ["username", "password1", "password2"]  # 사용자명과 비밀번호 입력 필드만 노출

# 프로젝트 등록 및 수정에 사용되는 폼 클래스
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project  # Project 모델 기반
        fields = ['title', 'description']  # 프로젝트 제목과 설명 입력 필드

# 평가 점수 입력을 위한 폼 클래스
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating  # Rating 모델 기반
        fields = ['score']  # 1~5 사이의 평가 점수 입력 필드