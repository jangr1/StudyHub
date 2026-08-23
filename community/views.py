# community/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count
from accounts.models import StudyRecord

def index_view(request):
    # 공개 설정(is_public=True)된 학습 기록만 최신순으로 조회
    public_records = StudyRecord.objects.filter(is_public=True).order_by('-created_at')
    total_community_likes = StudyRecord.objects.filter(is_public=True).aggregate(total=Count('likes'))['total'] or 0
    context = {
        'records': public_records,
        'total_community_likes': total_community_likes,
    }
    return render(request, 'community/index.html',context)

def home_view(request):
    # 1. 전체 공개된 기록 중 최신 3개만 미리보기로 추출
    recent_records = StudyRecord.objects.filter(is_public=True).order_by('-created_at')[:3]
    
    # 2. 메인 대시보드 요약 통계 계산
    total_records_count = StudyRecord.objects.count()
    total_minutes = StudyRecord.objects.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
    total_hours = round(total_minutes / 60, 1)
    active_users_count = StudyRecord.objects.values('user').distinct().count()

    context = {
        'recent_records': recent_records,
        'total_records_count': total_records_count,
        'total_hours': total_hours,
        'active_users_count': active_users_count,
    }
    return render(request, 'home.html', context)

@login_required
@require_POST
def like_record_view(request, record_id):
    record = get_object_or_404(StudyRecord, id=record_id, is_public=True)
    
    if request.user in record.likes.all():
        record.likes.remove(request.user)
    else:
        record.likes.add(request.user)

    # 요청이 들어온 이전 페이지(HTTP_REFERER)로 복귀, 없으면 커뮤니티 홈으로 이동
    return redirect(request.META.get('HTTP_REFERER', 'community:index'))