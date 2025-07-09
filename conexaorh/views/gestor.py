from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from itertools import chain
from conexaorh.forms import RequisicaoPessoalForm, MovimentacaoPessoalForm, RequisicaoDesligamentoForm, GestorPropostoMOV
from conexaorh.models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento

@login_required
def gestor_page(request):
    if request.user.user_type != 'gestor':
        return HttpResponseForbidden("Acesso negado! Apenas gestores podem acessar esta página.")

    form_rp = RequisicaoPessoalForm()
    form_movimentacao = MovimentacaoPessoalForm()
    form_rd = RequisicaoDesligamentoForm()
   
    
    movimentacao = MovimentacaoPessoal.objects.filter(
        complice_aprovacao="AUTORIZADO",
        gestor_proposto=request.user.username
    )
    
    form = GestorPropostoMOV()

    if request.method == "POST":
        if "submit_rp" in request.POST:
            form_rp = RequisicaoPessoalForm(request.POST, request.FILES)
            if form_rp.is_valid():
                form_rp.save(user=request.user)
                return redirect("gestor_page")
            
        elif "submit_movimentacao" in request.POST:
            form_movimentacao = MovimentacaoPessoalForm(request.POST, request.FILES)
            if form_movimentacao.is_valid():
                form_movimentacao.save(user=request.user, gestor_role="atual")
                return redirect("/gestor/?confirmacao=1")
        
        if "submit_aprovacao_mov" in request.POST:
            registro_id = request.POST.get("registro_id")
            if not registro_id:
                return HttpResponseBadRequest("ID do registro não informado.")
            
            registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
            form = GestorPropostoMOV(request.POST, request.FILES, instance=registro)

            if form.is_valid():
                form.save(user=request.user, gestor_role="proposto")
                assinatura = form.cleaned_data['assinatura_gestor_proposto']
                if assinatura:
                    registro.assinatura_gestor_proposto = assinatura
                    if registro.data_autorizacao_gestor_proposto is None:
                        registro.data_autorizacao_gestor_proposto = now()
                        registro.dias_para_autorizacao_gestor_proposto = (
                            now().date() - registro.data_solicitacao.date()
                        ).days
            return redirect("gestor_page")

        elif "submit_rd" in request.POST:
            form_rd = RequisicaoDesligamentoForm(request.POST, request.FILES)
            if form_rd.is_valid():
                form_rd.save(user=request.user)
                return redirect("/gestor/?confirmacao=1")
            

    context = {
        "form_rp": form_rp,
        "form_movimentacao": form_movimentacao,
        "form_rd": form_rd,
        "movimentacao": movimentacao,
        "form": form,
        "usuario": request.user,
    }

    if request.GET.get("confirmacao") == "1":
        context["abrir_confirmacao"] = True

    return render(request, "conexaorh/gestor/gestor.html", context)


@login_required
def movimentacoes_pendentes(request):
    if request.user.user_type != 'gestor':
        return HttpResponseForbidden("Acesso negado!")

    movimentacao = MovimentacaoPessoal.objects.filter(
        ~Q(assinatura_complice__isnull=True),
        ~Q(assinatura_complice=""),
        gestor_proposto=request.user.username
    )
    form = GestorPropostoMOV()

    if request.method == "POST" and "submit_aprovacao_mov" in request.POST:
        registro_id = request.POST.get("registro_id")
        if not registro_id:
            return HttpResponseBadRequest("ID do registro não informado.")
        
        registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
        form = GestorPropostoMOV(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            assinatura = form.cleaned_data['assinatura_gestor_proposto']
            if assinatura:
                registro.assinatura_gestor_proposto = assinatura
                if registro.data_autorizacao_gestor_proposto is None:
                    registro.data_autorizacao_gestor_proposto = now()
                    registro.dias_para_autorizacao_gestor_proposto = (
                        now().date() - registro.data_solicitacao.date()
                    ).days
                registro.save()
        return redirect("movimentacoes_pendentes")

    return render(request, "conexaorh/gestor/movimentacao.html", {
        "movimentacao": movimentacao,
        "form": form,
        "usuario": request.user,
    })

@login_required
def registros_gestor(request):
    rp = RequisicaoPessoal.objects.filter(
        Q(usuario=request.user) & ~Q(assinatura_rh__isnull=True) | ~Q(rh_aprovacao__iexact="PENDENTE")
    ).select_related("usuario")
    for r in rp:
        r.tipo = "RP"

    mov = MovimentacaoPessoal.objects.filter(
        Q(usuario=request.user) & ~Q(assinatura_rh__isnull=True)
    ).select_related("usuario")
    for m in mov:
        m.tipo = "MOV"

    rd = RequisicaoDesligamento.objects.filter(
        Q(usuario=request.user) & ~Q(assinatura_rh__isnull=True) 
    ).select_related("usuario")
    for d in rd:
        d.tipo = "RD"

    registros = sorted(
        chain(rp, mov, rd),
        key=lambda x: x.data_solicitacao,
        reverse=True
    )
    rp_pendente = RequisicaoPessoal.objects.filter(
        Q(usuario=request.user) & ~Q(assinatura_rh__isnull=False) & Q(rh_aprovacao__iexact="PENDENTE")
    ).select_related("usuario")
    for r in rp_pendente:
        r.tipo = "RP"

    mov_pendente = MovimentacaoPessoal.objects.filter(
        Q(usuario=request.user) & ~Q(assinatura_rh__isnull=False) & Q(rh_aprovacao__iexact="PENDENTE")
    ).select_related("usuario")
    for m in mov_pendente:
        m.tipo = "MOV"

    rd_pendente = RequisicaoDesligamento.objects.filter(
        Q(usuario=request.user) & ~Q(assinatura_rh__isnull=False) & Q(rh_aprovacao__iexact="PENDENTE")
    ).select_related("usuario")
    for d in rd_pendente:
        d.tipo = "RD"

    registros_pendentes = sorted (
        chain(rp_pendente, mov_pendente, rd_pendente),
        key = lambda x: x.data_solicitacao,
        reverse=True
    )
    return render(request, "conexaorh/gestor/registros_gestor.html", {
        "registros": registros,
        "registros_pendentes": registros_pendentes,
        "usuario": request.user  # opcional: para usar dados diretamente no template
    })