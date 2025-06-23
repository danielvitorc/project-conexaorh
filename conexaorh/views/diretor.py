from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from itertools import chain
from ..forms import DiretorForm, DiretorFormRD, DiretorFormMOV
from ..models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento

@login_required
def diretor_page(request):
    if request.user.user_type != "diretor":
        return HttpResponseForbidden("Acesso negado! Apenas diretores podem acessar esta página.")

    rp = RequisicaoPessoal.objects.all()
    movimentacao = MovimentacaoPessoal.objects.filter(~Q(assinatura_gestor_proposto__isnull=True))
    rd = RequisicaoDesligamento.objects.all()
    form = None

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        tipo_registro = request.POST.get("tipo_registro")  # Identifica o tipo

        if tipo_registro == "rp":
            registro = get_object_or_404(RequisicaoPessoal, id=registro_id)
            form_class = DiretorForm
        elif tipo_registro == "movimentacao":
            registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
        elif tipo_registro == "rd":
            registro = get_object_or_404(RequisicaoDesligamento, id=registro_id)
            form_class = DiretorFormRD
        else:
            return HttpResponseBadRequest("Tipo de registro inválido.")

        form = form_class(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
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

@login_required
def diretor_rp(request):
    if request.user.user_type != "diretor":
        return HttpResponseForbidden("Acesso negado!")

    registros = RequisicaoPessoal.objects.all()
    form = DiretorForm()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(RequisicaoPessoal, id=registro_id)
        form = DiretorForm(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
            
            if registro.assinatura_diretor and registro.data_autorizacao_diretor is None:
                registro.data_autorizacao_diretor = now()
                registro.dias_para_autorizacao_diretor = (
                    registro.data_autorizacao_diretor.date() - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("diretor_rp")

    return render(request, "conexaorh/diretor/rp.html", {"registros": registros, "form": form})


@login_required
def diretor_mov(request):
    if request.user.user_type != "diretor":
        return HttpResponseForbidden("Acesso negado!")

    registros = MovimentacaoPessoal.objects.filter(
        ~Q(assinatura_gestor_proposto__isnull=True)
    )
    form = DiretorFormMOV()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
        form = DiretorFormMOV(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
            if registro.assinatura_diretor and registro.data_autorizacao_diretor is None:
                registro.data_autorizacao_diretor = now()
                registro.dias_para_autorizacao_diretor = (
                    registro.data_autorizacao_diretor.date() - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("diretor_mov")

    return render(request, "conexaorh/diretor/mov.html", {"registros": registros, "form": form})

@login_required
def diretor_rd(request):
    if request.user.user_type != "diretor":
        return HttpResponseForbidden("Acesso negado!")

    registros = RequisicaoDesligamento.objects.all()
    form = DiretorFormRD()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(RequisicaoDesligamento, id=registro_id)
        form = DiretorFormRD(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
            if registro.assinatura_diretor and registro.data_autorizacao_diretor is None:
                registro.data_autorizacao_diretor = now()
                registro.dias_para_autorizacao_diretor = (
                    registro.data_autorizacao_diretor.date() - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("diretor_rd")

    return render(request, "conexaorh/diretor/rd.html", {"registros": registros, "form": form})

@login_required
def registros_diretor(request):
    rp = RequisicaoPessoal.objects.filter(
        ~Q(assinatura_rh__isnull=True)
    )
    for r in rp:
        r.tipo = "RP"

    mov = MovimentacaoPessoal.objects.filter(
        ~Q(assinatura_rh__isnull=True)
    )
    for m in mov:
        m.tipo = "MOV"
    
    rd = RequisicaoDesligamento.objects.filter(
        ~Q(assinatura_rh__isnull=True)
    )
    for d in rd:
        d.tipo = "RD"

    registros = sorted(
        chain(rp, mov, rd),
        key=lambda x: x.data_solicitacao,
        reverse=True
    )

    return render(request, "conexaorh/registros_diretor.html", {
        "registros": registros
    })