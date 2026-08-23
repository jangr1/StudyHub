from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    
     path('', views.index_view, name='index'),
     path('like/<int:record_id>/', views.like_record_view, name='like_record'),

     path('api/records/', views.api_record_list, name='api_records'),
    path('api/stats/', views.api_stats_summary, name='api_stats'),
]