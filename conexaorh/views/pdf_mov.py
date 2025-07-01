import os
from django.conf import settings
from django.utils.html import escape
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa
from ..models import MovimentacaoPessoal

def exportar_movimentacao_pdf(request):
    mov_id = request.GET.get("movimentacao")
    if not mov_id:
        messages.error(request, "ID da movimentação não fornecido.")
        return redirect("registros_gestor")

    movimentacao = get_object_or_404(MovimentacaoPessoal, id=mov_id)
    
    def get_absolute_image_url(image_field):
        if image_field:
            return request.build_absolute_uri(image_field.url)
        return None

    context = {
        "movimentacao": movimentacao,
        "now": datetime.now(),
        "assinatura_rh_url": get_absolute_image_url(movimentacao.imagem_assinatura_rh),
        "assinatura_gestor_url": get_absolute_image_url(movimentacao.imagem_assinatura_gestor_atual),
        "assinatura_gestor_proposto_url": get_absolute_image_url(movimentacao.imagem_assinatura_gestor_proposto),
        "assinatura_diretor_url": get_absolute_image_url(movimentacao.imagem_assinatura_diretor),
        "assinatura_presidente_url": get_absolute_image_url(movimentacao.imagem_assinatura_presidente),
        "assinatura_complice_url": get_absolute_image_url(movimentacao.imagem_assinatura_complice),

    }

    template = get_template("conexaorh/pdf/pdf_template_movimentacao.html")
    html = template.render(context)
    
    buffer = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=buffer)

    if pdf.err:
        messages.error(request, "Erro ao gerar PDF.")
        return redirect("registros_gestor")

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="movimentacao_{movimentacao.id}.pdf"'
    return response