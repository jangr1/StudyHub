# community/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count
from accounts.models import StudyRecord

def index_view(request):
    # ⚡ N+1 최적화: 1:N 관계(user)는 JOIN(select_related), M:N 관계(likes)는 prefetch_related로 일괄 조회
    records = (
        StudyRecord.objects.filter(is_public=True)
        .select_related('user')
        .prefetch_related('likes')
        .order_by('-created_at')
    )
    
    total_community_likes = StudyRecord.objects.filter(is_public=True).aggregate(total=Count('likes'))['total'] or 0

    context = {
        'records': records,
        'total_community_likes': total_community_likes,
    }
    return render(request, 'community/index.html', context)

def home_view(request):
    # 메인 홈 화면 최신 글 3개 조회 시에도 작성자 JOIN 최적화 적용
    recent_records = (
        StudyRecord.objects.filter(is_public=True)
        .select_related('user')
        .order_by('-created_at')[:3]
    )
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

    return redirect(request.META.get('HTTP_REFERER', 'community:index'))

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudyRecordSerializer

@api_view(['GET'])
def api_record_list(request):
    """
    공개된 공부 기록 목록을 JSON으로 반환하는 REST API
    """
    records = (
        StudyRecord.objects.filter(is_public=True)
        .select_related('user')
        .prefetch_related('likes')
        .order_by('-created_at')
    )
    serializer = StudyRecordSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_stats_summary(request):
    """
    플랫폼 전체 집계 데이터를 JSON으로 반환하는 REST API
    """
    total_records = StudyRecord.objects.count()
    total_minutes = StudyRecord.objects.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
    total_hours = round(total_minutes / 60, 1)
    active_users = StudyRecord.objects.values('user').distinct().count()

    return Response({
        'total_records': total_records,
        'total_study_hours': total_hours,
        'active_users': active_users,
    })