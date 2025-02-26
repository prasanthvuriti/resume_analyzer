from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.home, name='home'),  
    path('upload/', views.upload_resume, name='upload_resume'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path("analyze/", views.analyze_resume, name="analyze_resume"),  # Resume analysis
]

# Serve static files only in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Ensure media files are served
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
