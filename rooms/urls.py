from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('add/', views.room_add, name='room_add'),
    path('<int:pk>/', views.room_view, name='room_view'),
    path('<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('warden/', views.warden_room_list, name='warden_room_list'),
    path('warden/<int:pk>/', views.warden_room_view, name='warden_room_view'),
]
