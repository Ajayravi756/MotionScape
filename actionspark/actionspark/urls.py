from django.urls import path
from actionapp import views
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),  # This is the Django admin interface URL
    path('registration/', views.reg, name='registration'), 
    path('registration',views.reg),# Add this line to define the registration URL
    path('about/', views.about, name='about'),
    path('checkaction/', views.upload_video_view, name='checkaction'),
    path('statistics/', views.statistics, name='statistics'),
    path('logout/', views.LogoutPage, name='logout'),
    path('login/', views.login_view, name='login'),
    path('about_login/', views.about_login, name='about_login'), 
    path('statistics_login/', views.statistics_login, name='statistics_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Changed URL to avoid conflict
    path('approve_user_registration/<int:user_id>/', views.approve_user_registration, name='approve_user_registration'),
    path('reject_user_registration/<int:user_id>/', views.reject_user_registration, name='reject_user_registration'), 
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'), 
    path('admin_login/', views.admin_login, name='admin_login'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)