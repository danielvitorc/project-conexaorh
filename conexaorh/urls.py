from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('gestor/', gestor.gestor_page, name='gestor_page'),
    path('gestor/movimentacao/',gestor.movimentacoes_pendentes, name='movimentacoes_pendentes'),
    path('registros_gestor/', gestor.registros_gestor, name='registros_gestor'),
    path('diretor/', diretor.diretor_page, name='diretor_page'),
    path('registros_diretor/', diretor.registros_diretor, name='registros_diretor'),
    path("diretor/rp/", diretor.diretor_rp, name="diretor_rp"),
    path("diretor/movimentacao/", diretor.diretor_mov, name="diretor_mov"),
    path("diretor/rd/", diretor.diretor_rd, name="diretor_rd"),
    path('presidente/', presidente.presidente_page, name='presidente_page'),
    path("presidente/rp/", presidente.presidente_rp, name="presidente_rp"),
    path("presidente/movimentacao/", presidente.presidente_mov, name="presidente_mov"),
    path("presidente/rd/", presidente.presidente_rd, name="presidente_rd"),
    path('registros_presidente/', presidente.registros_presidente, name='registros_presidente'),
    path('rh/', rh.rh_page, name='rh_page'),
    path("rh/rp/", rh.rh_rp, name="rh_rp"),
    path("rh/movimentacao/", rh.rh_mov, name="rh_mov"),
    path("rh/rd/", rh.rh_rd, name="rh_rd"),
    path('registros_rh/', rh.registros_rh, name='registros_rh'),
    path('complice/', complice.complice_page, name='complice_page'),
    path('registros_complice/', complice.registros_complice, name='registros_complice'),
    path('download_rp/<int:registro_id>/', excel_rp.download_rp_excel, name='download_rp_excel'),
    path('download_mov/<int:registro_id>/', excel_mov.download_mov_excel, name='download_mov_excel'),
    path('download_rd/<int:registro_id>/', excel_rd.download_rd_excel, name='download_rd_excel'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)