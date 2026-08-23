from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    
     path('', views.index_view, name='index'),
     path('like/<int:record_id>/', views.like_record_view, name='like_record'),
]