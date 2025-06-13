from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from ..forms import PresidenteForm
from ..models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento

@login_required
def presidente_page(request):
    if request.user.user_type != "presidente":
        return HttpResponseForbidden("Acesso negado! Apenas presidentes podem acessar esta página.")

    rp = RequisicaoPessoal.objects.filter(~Q(assinatura_diretor__isnull=True), ~Q(assinatura_diretor=""))
    movimentacao = MovimentacaoPessoal.objects.filter(~Q(assinatura_diretor__isnull=True), ~Q(assinatura_diretor=""))
    rd = RequisicaoDesligamento.objects.filter(~Q(assinatura_diretor__isnull=True), ~Q(assinatura_diretor=""))

    form = PresidenteForm()
    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        tipo_registro = request.POST.get("tipo_registro")

        if tipo_registro == "rp":
            registro = get_object_or_404(RequisicaoPessoal, id=registro_id)
        elif tipo_registro == "movimentacao":
            registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
        elif tipo_registro == "rd":
            registro = get_object_or_404(RequisicaoDesligamento, id=registro_id)
        else:
            return HttpResponseBadRequest("Tipo de registro inválido.")

        form = PresidenteForm(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            # se acabou de assinar
            if registro.assinatura_presidente and registro.data_autorizacao_presidente is None:
                registro.data_autorizacao_presidente = now()
                registro.dias_para_autorizacao_presidente = (
                    registro.data_autorizacao_presidente.date()
                    - registro.data_solicitacao.date()
                ).days
            registro.save()
            
            return redirect("presidente_page")

    return render(
        request, 
        "conexaorh/presidente.html", 
        {"rp": rp, "movimentacao": movimentacao, "rd": rd, "usuario": request.user, "form": form}
    )