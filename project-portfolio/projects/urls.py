from django.urls import path
from . import views  # 현재 디렉토리의 views.py 불러오기

urlpatterns = [
    # 사용자 회원가입 페이지
    path("register/", views.register, name="register"),

    # 새 프로젝트 등록 페이지 (로그인 필요)
    path("create/", views.project_create, name="project_create"),

    # 특정 프로젝트 수정 페이지 (pk는 프로젝트 기본키, 로그인 필요)
    path("<int:pk>/update/", views.project_update, name="project_update"),

    # 특정 프로젝트 삭제 요청 처리 (pk는 프로젝트 기본키, 로그인 필요)
    path("<int:pk>/delete/", views.project_delete, name="project_delete"),

    # 특정 프로젝트 상세 페이지 (pk는 프로젝트 기본키)
    path("<int:pk>/", views.project_detail, name="project_detail"),

    # 프로젝트 평균 평점 기반 랭킹 목록
    path("ranking/", views.project_ranking, name="project_ranking"),

    # 프로젝트 전체 목록 (정렬 가능) — 사이트 기본 루트
    path("", views.project_list, name="project_list"),

    # 관리자 전용 프로젝트 대시보드
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]