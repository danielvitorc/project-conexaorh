from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from ..forms import DiretorForm
from ..models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento

@login_required
def diretor_page(request):
    if request.user.user_type != "diretor":
        return HttpResponseForbidden("Acesso negado! Apenas diretores podem acessar esta página.")

    rp = RequisicaoPessoal.objects.all()
    movimentacao = MovimentacaoPessoal.objects.filter(~Q(assinatura_gestor_proposto__isnull=True), ~Q(assinatura_gestor_proposto=""))
    rd = RequisicaoDesligamento.objects.all()


    form = DiretorForm()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        tipo_registro = request.POST.get("tipo_registro")  # Identifica o tipo

        if tipo_registro == "rp":
            registro = get_object_or_404(RequisicaoPessoal, id=registro_id)
        elif tipo_registro == "movimentacao":
            registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
        elif tipo_registro == "rd":
            registro = get_object_or_404(RequisicaoDesligamento, id=registro_id)
        else:
            return HttpResponseBadRequest("Tipo de registro inválido.")

        form = DiretorForm(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            # se acabou de assinar
            if registro.assinatura_diretor and registro.data_autorizacao_diretor is None:
                registro.data_autorizacao_diretor = now()
                registro.dias_para_autorizacao_diretor = (
                    registro.data_autorizacao_diretor.date()
                    - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("diretor_page")

    return render(request, "conexaorh/diretor.html", {"rp": rp, "movimentacao": movimentacao, "rd": rd, "usuario": request.user, "form": form})