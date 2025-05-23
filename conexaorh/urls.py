from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('gestor/', views.gestor_page, name='gestor_page'),
    path('diretor/', views.diretor_page, name='diretor_page'),
    path('presidente/', views.presidente_page, name='presidente_page'),
    path('rh/', views.rh_page, name='rh_page'),
    path('complice/', views.complice_page, name='complice_page'),
    path('download_rp/<int:registro_id>/', views.download_rp_excel, name='download_rp_excel'),
    path('download_mov/<int:registro_id>/', views.download_mov_excel, name='download_mov_excel'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)