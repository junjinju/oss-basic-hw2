from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# 기본 Django User 모델을 사용
class User(AbstractUser):
    pass


# 프로젝트 정보를 저장하기 위한 모델
class Project(models.Model):
    # 프로젝트 소유자 (User 모델과 Many-to-One 관계)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 프로젝트 제목
    title = models.CharField(max_length=255)

    # 프로젝트 설명
    description = models.TextField()

    # 생성 시간
    created_at = models.DateTimeField(auto_now_add=True)

    # 수정 시간
    updated_at = models.DateTimeField(auto_now=True)

    # 프로젝트에 대한 평균 평점을 계산하는 메서드
    def average_rating(self):
        ratings = self.ratings.all()  
        # 평점이 존재하면 평균을 소수점 둘째 자리까지 반환, 없으면 0 반환
        return round(sum(r.score for r in ratings) / ratings.count(), 2) if ratings else 0

# 평점 정보를 저장하기 위한 모델
class Rating(models.Model):
    # 평점을 남긴 대상 프로젝트 (Project 모델과 Many-to-One 관계)
    project = models.ForeignKey(Project, related_name='ratings', on_delete=models.CASCADE)

    # 평점을 남긴 사용자 (User 모델과 Many-to-One 관계)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 평점 점수 (1부터 5까지 가능)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    # 동일한 유저가 같은 프로젝트에 대해 중복 평가하지 못하도록 제한
    class Meta:
        unique_together = ('project', 'user')  # (project, user) 쌍에 대한 Unique 제약 조건