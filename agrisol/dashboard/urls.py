import dashboard.routing
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('profil/', views.profil, name='profil'),
    path('change_password/', views.change_password, name='change_password'),
    path('temperature/', views.temperature_dashboard, name='temperature'),
    
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/<int:culture_id>/', views.dashboard_view, name='dashboard'),
    
    path('mes-cultures/', views.mes_cultures, name='mes_cultures'),
    path('delete_culture/<int:culture_id>/', views.delete_culture, name='delete_culture'),
    path('alert/', views.alert, name='alert'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
