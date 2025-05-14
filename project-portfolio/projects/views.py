from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Rating
from .forms import ProjectForm, RatingForm, UserRegisterForm
from django.contrib.auth import login
from django.db.models import Avg
from django.contrib.admin.views.decorators import staff_member_required


# 사용자 회원가입 뷰
def register(request):
    if request.method == "POST":
        # POST 요청이면 폼 데이터를 전달받아 폼 객체 생성
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # 유효한 입력인 경우, 사용자 저장 및 자동 로그인 처리
            user = form.save()
            login(request, user)
            return redirect("project_list")  # 회원가입 후 프로젝트 목록 페이지로 이동
    else:
        # GET 요청 시 회원가입 폼 생성
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


# 프로젝트 생성 뷰 (로그인한 사용자만 접근 가능)
@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)  # 폼에서 받은 데이터를 기반으로 새로운 프로젝트 객체 생성
        project.user = request.user        # 현재 로그인한 사용자를 소유자로 설정
        project.save()                     # 실제 DB 저장
        return redirect("project_list")    # 생성 후 프로젝트 목록으로 이동
    return render(request, "project_form.html", {"form": form})


# 프로젝트 수정 뷰 (소유자 또는 관리자가 접근 가능)
@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # 소유자 본인 또는 관리자만 수정 가능
    if request.user != project.user and not request.user.is_staff:
        return redirect("project_list")

    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect("project_list")
    return render(request, "project_form.html", {"form": form})


# 프로젝트 삭제 뷰 (소유자 또는 관리자만 삭제 가능)
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user == project.user or request.user.is_staff:
        project.delete()
    return redirect("project_list")


# 전체 프로젝트 목록을 정렬 기준에 따라 표시하는 뷰
def project_list(request):
    sort = request.GET.get("sort", "name")  # 기본 정렬은 이름순

    if sort == "recent":
        # 최신순 정렬 (작성일 내림차순)
        projects = Project.objects.annotate(avg_score=Avg("ratings__score")).order_by("-created_at")
    elif sort == "score":
        # 평균 평점순 정렬
        projects = Project.objects.annotate(avg_score=Avg("ratings__score")).order_by("-avg_score")
    else:
        # 이름순 정렬
        projects = Project.objects.annotate(avg_score=Avg("ratings__score")).order_by("title")

    return render(request, "project_list.html", {
        "projects": projects,
        "sort": sort,
    })


# 프로젝트 상세 페이지 및 평점 등록 처리 뷰
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # 사용자가 과거에 평가한 적 있는지 확인
    rating_given = Rating.objects.filter(user=request.user, project=project).exists() if request.user.is_authenticated else False

    if request.method == "POST" and not rating_given:
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user       # 현재 사용자로 설정
            rating.project = project         # 평가 대상 프로젝트 지정
            rating.save()
            return redirect("project_detail", pk=pk)
    else:
        form = RatingForm()

    return render(request, "project_detail.html", {
        "project": project,
        "form": form,
        "rating_given": rating_given
    })


# 평균 평점 기준으로 프로젝트를 정렬해 보여주는 랭킹 뷰
def project_ranking(request):
    projects = Project.objects.annotate(avg_score=Avg("ratings__score")).order_by("-avg_score")
    return render(request, "ranking.html", {"projects": projects})


# 관리자 전용 대시보드 뷰
@staff_member_required
def admin_dashboard(request):
    projects = Project.objects.annotate(avg_score=Avg("ratings__score")).order_by("-avg_score")
    return render(request, "admin_dashboard.html", {"projects": projects})