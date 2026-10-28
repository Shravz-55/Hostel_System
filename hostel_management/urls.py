"""
URL configuration for hostel_management project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('rooms/', include('rooms.urls')),
    path('fees/', include('fees.urls')),
    path('complaints/', include('complaints.urls')),
    path('notice/', include('notice.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
