from django.urls import path
from .views import *
from .views import pdf_rp, pdf_mov, pdf_rd
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('gestor/', gestor.gestor_page, name='gestor_page'),
    path('ajax/bases-gestor/', gestor.carregar_bases, name='ajax_carregar_bases'),
    path('ajax/departamentos/', gestor.carregar_departamentos, name='ajax_carregar_departamentos'),
    path('ajax/cargos/', gestor.carregar_cargos, name='ajax_carregar_cargos'),
    path('ajax/cursos-do-cargo/', gestor.carregar_cursos_do_cargo, name='ajax_cursos_do_cargo'),
    path('gestor/movimentacao/', gestor.movimentacoes_pendentes, name='movimentacoes_pendentes'),
    path('registros_gestor/', gestor.registros_gestor, name='registros_gestor'),
    path('diretor/', diretor.diretor_page, name='diretor_page'),
    path("diretor/rp/", diretor.diretor_rp, name="diretor_rp"),
    path("diretor/movimentacao/", diretor.diretor_mov, name="diretor_mov"),
    path("diretor/rd/", diretor.diretor_rd, name="diretor_rd"),
    path('presidente/', presidente.presidente_page, name='presidente_page'),
    path("presidente/rp/", presidente.presidente_rp, name="presidente_rp"),
    path("presidente/movimentacao/", presidente.presidente_mov, name="presidente_mov"),
    path("presidente/rd/", presidente.presidente_rd, name="presidente_rd"),
    path('registros_presidente/', presidente.registros_presidente, name='registros_presidente'),
    path('rh/', rh.rh_page, name='rh_page'),
    path('ajax/bases/', rh.bases_por_filial, name='bases_por_filial'),
    path("ajax/setores/", rh.setores_por_base, name="setores_por_base"),
    path('filial/editar/<int:pk>/', rh.editar_filial, name='editar_filial'),
    path("editar_filial/<int:pk>/", rh.editar_filial, name="editar_filial"),
    path("editar_base/<int:pk>/", rh.editar_base, name="editar_base"),
    path("editar_setor/<int:pk>/", rh.editar_setor, name="editar_setor"),
    path("editar_curso/<int:pk>/", rh.editar_curso, name="editar_curso"),
    path("editar_cargo/<int:pk>/", rh.editar_cargo, name="editar_cargo"),
    path('filial/excluir/<int:id>/', rh.excluir_filial, name='excluir_filial'),
    path('base/excluir/<int:id>/', rh.excluir_base, name='excluir_base'),
    path('setor/excluir/<int:id>/', rh.excluir_setor, name='excluir_setor'),
    path('curso/excluir/<int:id>/', rh.excluir_curso, name='excluir_curso'),
    path('cargo/excluir/<int:id>/', rh.excluir_cargo, name='excluir_cargo'),
    path("rh/rp/", rh.rh_rp, name="rh_rp"),
    path("rh/movimentacao/", rh.rh_mov, name="rh_mov"),
    path("rh/rd/", rh.rh_rd, name="rh_rd"),
    path('complice/', complice.complice_page, name='complice_page'),
    path('registros_complice/', complice.registros_complice, name='registros_complice'),
    path('download_rp/<int:registro_id>/', excel_rp.download_rp_excel, name='download_rp_excel'),
    path('download_mov/<int:registro_id>/', excel_mov.download_mov_excel, name='download_mov_excel'),
    path('download_rd/<int:registro_id>/', excel_rd.download_rd_excel, name='download_rd_excel'),
    path("exportar_requisicao_pdf/", pdf_rp.exportar_requisicao_pdf, name="exportar_requisicao_pdf"),
    path("exportar_movimentacao_pdf/", pdf_mov.exportar_movimentacao_pdf, name="exportar_movimentacao_pdf"),
    path("exportar_desligamento_pdf/", pdf_rd.exportar_desligamento_pdf, name="exportar_desligamento_pdf"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)