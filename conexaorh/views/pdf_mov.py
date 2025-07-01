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
        "assinatura_rh_url": movimentacao.imagem_assinatura_rh.url if movimentacao.imagem_assinatura_rh else None,
        "assinatura_gestor_url": movimentacao.imagem_assinatura_gestor_atual.url if movimentacao.imagem_assinatura_gestor_atual else None,
        "assinatura_gestor_proposto_url": movimentacao.imagem_assinatura_gestor_proposto.url if movimentacao.imagem_assinatura_gestor_proposto else None,
        "assinatura_diretor_url": movimentacao.imagem_assinatura_diretor.url if movimentacao.imagem_assinatura_diretor else None,
        "assinatura_presidente_url": movimentacao.imagem_assinatura_presidente.url if movimentacao.imagem_assinatura_presidente else None,
        "assinatura_complice_url": movimentacao.imagem_assinatura_complice.url if movimentacao.imagem_assinatura_complice else None,
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