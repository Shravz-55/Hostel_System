from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Admin URLs
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Warden Management (Admin)
    path('admin/wardens/', views.warden_list, name='warden_list'),
    path('admin/wardens/add/', views.warden_add, name='warden_add'),
    path('admin/wardens/delete/<int:pk>/', views.warden_delete, name='warden_delete'),

    # Warden URLs
    path('warden/login/', views.warden_login, name='warden_login'),
    path('warden/logout/', views.warden_logout, name='warden_logout'),
    path('warden/dashboard/', views.warden_dashboard, name='warden_dashboard'),

    # Student URLs
    path('student/login/', views.student_login, name='student_login'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/logout/', views.student_logout, name='student_logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]
