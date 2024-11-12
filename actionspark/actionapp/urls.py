from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
        path('', views.index_view, name='index'),
        
        path('checkaction/', views.upload_video_view, name='checkaction'),  # Change the URL path to 'checkaction',
        path('login/', views.login_view, name='login'),
        path('result/<int:video_id>/', views.result_view, name='result'),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
