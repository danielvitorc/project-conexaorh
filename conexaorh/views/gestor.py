from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from itertools import chain
from ..forms import RequisicaoPessoalForm, MovimentacaoPessoalForm, RequisicaoDesligamentoForm, GestorPropostoApprovalForm
from ..models import MovimentacaoPessoal, RequisicaoPessoal, RequisicaoDesligamento

@login_required
def gestor_page(request):
    if request.user.user_type != 'gestor':
        return HttpResponseForbidden("Acesso negado! Apenas gestores podem acessar esta página.")

    form_rp = RequisicaoPessoalForm()
    form_movimentacao = MovimentacaoPessoalForm()
    form_rd = RequisicaoDesligamentoForm()
   
    movimentacao = MovimentacaoPessoal.objects.filter(
        ~Q(assinatura_complice__isnull=True),
        gestor_proposto=request.user.username
    )
    form = GestorPropostoApprovalForm()

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
                return redirect("gestor_page")
        
        if "submit_aprovacao_mov" in request.POST:
            registro_id = request.POST.get("registro_id")
            if not registro_id:
                return HttpResponseBadRequest("ID do registro não informado.")
            
            registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
            form = GestorPropostoApprovalForm(request.POST, request.FILES, instance=registro)

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
                return redirect("gestor_page")
            

    return render(request, "conexaorh/gestor.html", {
        "form_rp": form_rp,
        "form_movimentacao": form_movimentacao,
        "form_rd": form_rd,
        "movimentacao": movimentacao,
        "form": form,
        "usuario": request.user,
    })

@login_required
def registros_gestor(request):
    rp = RequisicaoPessoal.objects.filter(
        Q(usuario=request.user) &
        ~Q(assinatura_rh__isnull=True)
    )
    for r in rp:
        r.tipo = "RP"

    mov = MovimentacaoPessoal.objects.filter(
        Q(usuario=request.user) &
        ~Q(assinatura_rh__isnull=True)
    )
    for m in mov:
        m.tipo = "MOV"
    
    rd = RequisicaoDesligamento.objects.filter(
        Q(usuario=request.user) &
        ~Q(assinatura_rh__isnull=True)
    )
    for d in rd:
        d.tipo = "RD"

    registros = sorted(
        chain(rp, mov, rd),
        key=lambda x: x.data_solicitacao,
        reverse=True
    )

    return render(request, "conexaorh/registros_gestor.html", {
        "registros": registros
    })

@login_required
def assinar_requisicao_gestor(request, requisicao_id):
    requisicao = get_object_or_404(RequisicaoPessoal, id=requisicao_id)

    if requisicao.assinatura_gestor:
        messages.warning(request, "Esta requisição já foi assinada.")
    else:
        requisicao.assinar_gestor(request.user)
        messages.success(request, "Requisição assinada com sucesso.")

    return redirect('pagina_requisicao', requisicao_id=requisicao.id)  # redirecione para onde preferir
