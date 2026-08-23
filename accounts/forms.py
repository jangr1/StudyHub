# accounts/forms.py
from django import forms
from .models import UserProfile, StudyRecord

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'department']
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '한줄 소개를 입력하세요'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전공/공부 분야'}),
        }

class StudyRecordForm(forms.ModelForm):
    class Meta:
        model = StudyRecord
        fields = ['subject', 'duration_minutes', 'memo', 'is_public']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 알고리즘, VHDL'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '분 단위 (예: 60)'}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '오늘 공부한 내용을 적어보세요'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }