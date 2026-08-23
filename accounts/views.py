import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import UserProfile, StudyRecord
from .forms import UserProfileForm, StudyRecordForm

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:mypage')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 회원가입 즉시 프로필 생성 및 자동 로그인
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('accounts:mypage')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:mypage')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:mypage')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# --- 마이페이지 및 기록 관리 뷰 ---

@login_required
def mypage_view(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            profile_form = UserProfileForm(request.POST, instance=profile)
            record_form = StudyRecordForm()
            if profile_form.is_valid():
                profile_form.save()
                return redirect('accounts:mypage')

        elif action == 'add_record':
            profile_form = UserProfileForm(instance=profile)
            record_form = StudyRecordForm(request.POST)
            if record_form.is_valid():
                record = record_form.save(commit=False)
                record.user = user
                record.is_public = 'is_public' in request.POST
                record.save()
                return redirect('accounts:mypage')
        else:
            profile_form = UserProfileForm(instance=profile)
            record_form = StudyRecordForm()
    else:
        profile_form = UserProfileForm(instance=profile)
        record_form = StudyRecordForm()

    records = StudyRecord.objects.filter(user=user).order_by('-id')

    # --- 📊 1. 과목별 누적 공부 시간 집계 (도넛 차트용) ---
    subject_data = (
        StudyRecord.objects.filter(user=user)
        .values('subject')
        .annotate(total_minutes=Sum('duration_minutes'))
        .order_by('-total_minutes')
    )
    subject_labels = [item['subject'] for item in subject_data]
    subject_times = [item['total_minutes'] for item in subject_data]

    # --- 📊 2. 최근 7일간 일별 공부 시간 집계 (막대 차트용) ---
    today = timezone.now().date()
    daily_labels = []
    daily_times = []

    for i in range(6, -1, -1):
        target_date = today - timedelta(days=i)
        daily_labels.append(target_date.strftime('%m/%d'))
        
        day_minutes = (
            StudyRecord.objects.filter(user=user, created_at__date=target_date)
            .aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        )
        daily_times.append(day_minutes)

    context = {
        'profile': profile,
        'profile_form': profile_form,
        'record_form': record_form,
        'records': records,
        'subject_labels_json': json.dumps(subject_labels),
        'subject_times_json': json.dumps(subject_times),
        'daily_labels_json': json.dumps(daily_labels),
        'daily_times_json': json.dumps(daily_times),
    }
    return render(request, 'accounts/mypage.html', context)


@login_required
@require_POST
def delete_record_view(request, record_id):
    record = get_object_or_404(StudyRecord, id=record_id, user=request.user)
    record.delete()
    return redirect('accounts:mypage')


@login_required
def edit_record_view(request, record_id):
    record = get_object_or_404(StudyRecord, id=record_id, user=request.user)

    if request.method == 'POST':
        form = StudyRecordForm(request.POST, instance=record)
        if form.is_valid():
            updated_record = form.save(commit=False)
            updated_record.is_public = 'is_public' in request.POST
            updated_record.save()
            return redirect('accounts:mypage')
    else:
        form = StudyRecordForm(instance=record)

    context = {
        'form': form,
        'record': record,
    }
    return render(request, 'accounts/edit_record.html', context)