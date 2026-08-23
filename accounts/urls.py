from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('record/<int:record_id>/delete/', views.delete_record_view, name='delete_record'),
    path('record/<int:record_id>/edit/', views.edit_record_view, name='edit_record'),
]