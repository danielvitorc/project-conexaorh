from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('gestor/', gestor.gestor_page, name='gestor_page'),
    path('registros_gestor/', gestor.registros_gestor, name='registros_gestor'),
    path('diretor/', diretor.diretor_page, name='diretor_page'),
    path('registros_diretor/', diretor.registros_diretor, name='registros_diretor'),
    path('presidente/', presidente.presidente_page, name='presidente_page'),
    path('registros_presidente/', presidente.registros_presidente, name='registros_presidente'),
    path('rh/', rh.rh_page, name='rh_page'),
    path('registros_rh/', rh.registros_rh, name='registros_rh'),
    path('complice/', complice.complice_page, name='complice_page'),
    path('download_rp/<int:registro_id>/', excel_rp.download_rp_excel, name='download_rp_excel'),
    path('download_mov/<int:registro_id>/', excel_mov.download_mov_excel, name='download_mov_excel'),
    path('download_rd/<int:registro_id>/', excel_rd.download_rd_excel, name='download_rd_excel'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)