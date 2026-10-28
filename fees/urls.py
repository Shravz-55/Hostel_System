from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    # Admin URLs
    path('', views.fee_list, name='fee_list'),
    path('add/', views.fee_add, name='fee_add'),
    path('<int:pk>/mark-paid/', views.fee_mark_paid, name='fee_mark_paid'),
    path('<int:pk>/delete/', views.fee_delete, name='fee_delete'),

    # Warden URLs
    path('warden/', views.warden_fee_list, name='warden_fee_list'),
    path('warden/add/', views.warden_fee_add, name='warden_fee_add'),
    path('warden/<int:pk>/mark-paid/', views.warden_fee_mark_paid, name='warden_fee_mark_paid'),

    # Student URLs
    path('student/', views.student_fee_list, name='student_fee_list'),
    path('student/<int:pk>/pay/', views.student_pay_fee, name='student_pay_fee'),
]
