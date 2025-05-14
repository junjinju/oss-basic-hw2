from django.contrib import admin
from .models import Project, Rating, User

# Project 모델을 기본 관리자 페이지에 등록하며, 리스트에 표시할 필드를 정의
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'average_rating')  # 프로젝트 제목, 작성자, 등록일, 평균 점수 표시

# Rating 모델을 기본 관리자 페이지에 등록하며, 리스트에 표시할 필드를 정의
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'score')  # 어떤 프로젝트에 누가 몇 점을 줬는지 표시

# 사용자 모델(User)을 기본 관리자 페이지에 등록
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')  # 사용자명, 이메일, 스태프 여부, 슈퍼유저 여부 표시