from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    # Admin URLs
    path('', views.notice_list, name='notice_list'),
    path('add/', views.notice_add, name='notice_add'),
    path('<int:pk>/', views.notice_view, name='notice_view'),
    path('<int:pk>/delete/', views.notice_delete, name='notice_delete'),

    # Student URLs
    path('student/', views.student_notice_list, name='student_notice_list'),
    path('student/<int:pk>/', views.student_notice_view, name='student_notice_view'),
]
