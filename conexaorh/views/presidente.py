from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from itertools import chain
from ..forms import PresidenteForm, PresidenteFormRD, PresidenteFormMOV
from ..models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento

@login_required
def presidente_page(request):
    if request.user.user_type != "presidente":
        return HttpResponseForbidden("Acesso negado! Apenas presidentes podem acessar esta página.")

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

    return render(request, "conexaorh/presidente/presidente.html", {
        "registros": registros, "usuario": request.user,
    })
@login_required
def presidente_rp(request):
    if request.user.user_type != "presidente":
        return HttpResponseForbidden("Acesso Negado!")
    
    registros = RequisicaoPessoal.objects.filter(diretor_aprovacao="AUTORIZADO").order_by('-data_solicitacao')
    form = PresidenteForm()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(RequisicaoPessoal, id=registro_id)
        form = PresidenteForm(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
            # se acabou de assinar
            if registro.assinatura_presidente and registro.data_autorizacao_presidente is None:
                registro.data_autorizacao_presidente = now()
                registro.dias_para_autorizacao_presidente = (
                    registro.data_autorizacao_presidente.date()
                    - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("presidente_rp")

    return render(request, "conexaorh/presidente/rp.html", {"registros": registros, "usuario": request.user, "form": form})


@login_required
def presidente_mov(request):
    if request.user.user_type != "presidente":
        return HttpResponseForbidden("Acesso Negado!")
    
    registros = MovimentacaoPessoal.objects.filter(diretor_aprovacao="AUTORIZADO").order_by('-data_solicitacao')
    form = PresidenteFormMOV()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
        form = PresidenteFormMOV(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
            # se acabou de assinar
            if registro.assinatura_presidente and registro.data_autorizacao_presidente is None:
                registro.data_autorizacao_presidente = now()
                registro.dias_para_autorizacao_presidente = (
                    registro.data_autorizacao_presidente.date()
                    - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("presidente_mov")

    return render(request, "conexaorh/presidente/mov.html", {"registros": registros, "usuario": request.user,"form": form})

@login_required
def presidente_rd(request):
    if request.user.user_type != "presidente":
        return HttpResponseForbidden("Acesso Negado!")
    
    registros = RequisicaoDesligamento.objects.filter(diretor_aprovacao="AUTORIZADO").order_by('-data_solicitacao')
    form = PresidenteFormRD()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(RequisicaoDesligamento, id=registro_id)
        form = PresidenteFormRD(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
            # se acabou de assinar
            if registro.assinatura_presidente and registro.data_autorizacao_presidente is None:
                registro.data_autorizacao_presidente = now()
                registro.dias_para_autorizacao_presidente = (
                    registro.data_autorizacao_presidente.date()
                    - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("presidente_rd")

    return render(request, "conexaorh/presidente/rd.html", {"registros": registros, "usuario": request.user,"form": form})

@login_required
def registros_presidente(request):
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

    return render(request, "conexaorh/presidente/registros_presidente.html", {
        "registros": registros, "usuario": request.user,
    })