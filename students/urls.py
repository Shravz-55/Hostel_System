from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Admin URLs
    path('', views.student_list, name='student_list'),
    path('add/', views.student_add, name='student_add'),
    path('<int:pk>/', views.student_view, name='student_view'),
    path('<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('<int:pk>/assign-room/', views.student_assign_room, name='student_assign_room'),
    path('<int:pk>/vacate-room/', views.student_vacate_room, name='student_vacate_room'),

    # Warden URLs
    path('warden/', views.warden_student_list, name='warden_student_list'),
    path('warden/<int:pk>/', views.warden_student_view, name='warden_student_view'),
]
