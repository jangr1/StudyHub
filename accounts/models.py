
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    사용자의 추가 프로필 정보 (1:1 관계)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=150, blank=True, verbose_name="한줄 소개")
    department = models.CharField(max_length=50, blank=True, verbose_name="공부 분야/전공")

    def __str__(self):
        return f"{self.user.username}의 프로필"


class StudyRecord(models.Model):
    """
    마이페이지의 개인 공부 기록 (1:N 관계)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_records')
    subject = models.CharField(max_length=100, verbose_name="과목/주제")
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name="공부 시간(분)")
    memo = models.TextField(blank=True, verbose_name="학습 내용 및 메모")
    
    # 커뮤니티 공유 여부 (True면 다른 유저에게도 공개 가능)
    is_public = models.BooleanField(default=False, verbose_name="커뮤니티 공유 여부")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="기록 일시")

    likes = models.ManyToManyField(User, related_name='liked_records', blank=True)

    class Meta:
        ordering = ['-created_at']  # 최신 기록이 먼저 오도록 정렬

    def __str__(self):
        return f"[{self.user.username}] {self.subject} ({self.duration_minutes}분)"