from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    # Admin URLs
    path('', views.complaint_list, name='complaint_list'),
    path('<int:pk>/', views.complaint_view, name='complaint_view'),
    path('<int:pk>/resolve/', views.complaint_resolve, name='complaint_resolve'),

    # Warden URLs
    path('warden/', views.warden_complaint_list, name='warden_complaint_list'),
    path('warden/<int:pk>/', views.warden_complaint_view, name='warden_complaint_view'),
    path('warden/<int:pk>/resolve/', views.warden_complaint_resolve, name='warden_complaint_resolve'),

    # Student URLs
    path('student/', views.student_complaint_list, name='student_complaint_list'),
    path('student/add/', views.student_complaint_add, name='student_complaint_add'),
    path('student/<int:pk>/', views.student_complaint_view, name='student_complaint_view'),
]
