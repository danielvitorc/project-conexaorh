from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa
from ..models import RequisicaoDesligamento

def exportar_desligamento_pdf(request):
    desligamento_id = request.GET.get("desligamento")
    if not desligamento_id:
        messages.error(request, "ID da requisição de desligamento não fornecido.")
        return redirect("registros_gestor")

    desligamento = get_object_or_404(RequisicaoDesligamento, id=desligamento_id)

    def get_absolute_image_url(image_field):
        if image_field:
            return request.build_absolute_uri(image_field.url)
        return None

    context = {
        "desligamento": desligamento,
        "now": datetime.now(),
        "assinatura_gestor_url": get_absolute_image_url(desligamento.imagem_assinatura_gestor),
        "assinatura_diretor_url": get_absolute_image_url(desligamento.imagem_assinatura_diretor),
        "assinatura_presidente_url": get_absolute_image_url(desligamento.imagem_assinatura_presidente),
        "assinatura_rh_url": get_absolute_image_url(desligamento.imagem_assinatura_rh),
    }

    template = get_template("conexaorh/pdf/pdf_template_desligamento.html")
    html = template.render(context)

    buffer = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=buffer)

    if pdf.err:
        messages.error(request, "Erro ao gerar PDF.")
        return redirect("registros_gestor")

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    filename = f"desligamento_{desligamento.id}.pdf"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
