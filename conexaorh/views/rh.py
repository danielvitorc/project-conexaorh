from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from itertools import chain
from ..forms import  RHForm, RHFormRD, RHFormMOV
from ..models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento

@login_required
def rh_page(request):
    if request.user.user_type != "rh":
        return HttpResponseForbidden("Acesso negado! Apenas usuários do RH podem acessar esta página.")

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

    return render(request, "conexaorh/rh/rh.html", {
        "registros": registros, "usuario": request.user,
    })


@login_required
def rh_rp(request):
    if request.user.user_type != "rh":
        return HttpResponseForbidden("Acesso negado!")

    registros = RequisicaoPessoal.objects.filter(~Q(assinatura_presidente__isnull=True))
    form = RHForm()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(RequisicaoPessoal, id=registro_id)
        form = RHForm(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            # se acabou de assinar
            if registro.assinatura_rh and registro.data_autorizacao_rh is None:
                registro.data_autorizacao_rh = now()
                registro.dias_para_autorizacao_rh = (
                    registro.data_autorizacao_rh.date()
                    - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("rh_rp")

    return render(request, "conexaorh/rh/rp.html", {"registros": registros,"usuario": request.user, "form": form})

@login_required
def rh_rp(request):
    if request.user.user_type != "rh":
        return HttpResponseForbidden("Acesso negado!")

    registros = RequisicaoPessoal.objects.filter(~Q(assinatura_presidente__isnull=True))  
    form = RHForm()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(RequisicaoPessoal, id=registro_id)
        form = RHForm(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
            # se acabou de assinar
            if registro.assinatura_rh and registro.data_autorizacao_rh is None:
                registro.data_autorizacao_rh = now()
                registro.dias_para_autorizacao_rh = (
                    registro.data_autorizacao_rh.date()
                    - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("rh_rp")

    return render(request, "conexaorh/rh/rp.html", {"registros": registros,"usuario": request.user, "form": form})

@login_required
def rh_mov(request):
    if request.user.user_type != "rh":
        return HttpResponseForbidden("Acesso negado!")

    registros = RequisicaoDesligamento.objects.filter(~Q(assinatura_presidente__isnull=True))   
    form = RHFormMOV()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
        form = RHFormMOV(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
            # se acabou de assinar
            if registro.assinatura_rh and registro.data_autorizacao_rh is None:
                registro.data_autorizacao_rh = now()
                registro.dias_para_autorizacao_rh = (
                    registro.data_autorizacao_rh.date()
                    - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("rh_mov")

    return render(request, "conexaorh/rh/mov.html", {"registros": registros,"usuario": request.user, "form": form})

@login_required
def rh_rd(request):
    if request.user.user_type != "rh":
        return HttpResponseForbidden("Acesso negado!")

    registros = RequisicaoDesligamento.objects.filter(~Q(assinatura_presidente__isnull=True))  
    form = RHFormRD()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(RequisicaoDesligamento, id=registro_id)
        form = RHFormRD(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            form.save(user=request.user)
            # se acabou de assinar
            if registro.assinatura_rh and registro.data_autorizacao_rh is None:
                registro.data_autorizacao_rh = now()
                registro.dias_para_autorizacao_rh = (
                    registro.data_autorizacao_rh.date()
                    - registro.data_solicitacao.date()
                ).days
            registro.save()
            return redirect("rh_rd")

    return render(request, "conexaorh/rh/rd.html", {"registros": registros,"usuario": request.user, "form": form})

