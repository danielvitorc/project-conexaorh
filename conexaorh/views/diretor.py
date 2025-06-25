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

    rp = RequisicaoPessoal.objects.filter(
        ~Q(assinatura_rh__isnull=True)
    ).select_related("usuario")
    for r in rp:
        r.tipo = "RP"

    mov = MovimentacaoPessoal.objects.filter(
        ~Q(assinatura_rh__isnull=True)
    ).select_related("usuario")
    for m in mov:
        m.tipo = "MOV"
    
    rd = RequisicaoDesligamento.objects.filter(
        ~Q(assinatura_rh__isnull=True)
    ).select_related("usuario")
    for d in rd:
        d.tipo = "RD"

    registros = sorted(
        chain(rp, mov, rd),
        key=lambda x: x.data_solicitacao,
        reverse=True
    )

    return render(request, "conexaorh/diretor/diretor.html", {
        "registros": registros,
        "usuario": request.user 
    })


@login_required
def diretor_rp(request):
    if request.user.user_type != "diretor":
        return HttpResponseForbidden("Acesso negado!")

    registros = RequisicaoPessoal.objects.all().select_related("usuario").order_by('-data_solicitacao')
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

    return render(request, "conexaorh/diretor/rp.html", {"registros": registros, "form": form, "usuario": request.user})


@login_required
def diretor_mov(request):
    if request.user.user_type != "diretor":
        return HttpResponseForbidden("Acesso negado!")

    registros = MovimentacaoPessoal.objects.filter(gestor_proposto_aprovacao="AUTORIZADO").order_by('-data_solicitacao')
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

    return render(request, "conexaorh/diretor/mov.html", {"registros": registros, "form": form, "usuario": request.user})


@login_required
def diretor_rd(request):
    if request.user.user_type != "diretor":
        return HttpResponseForbidden("Acesso negado!")

    registros = RequisicaoDesligamento.objects.all().order_by('-data_solicitacao')
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

    return render(request, "conexaorh/diretor/rd.html", {"registros": registros, "form": form, "usuario": request.user})


