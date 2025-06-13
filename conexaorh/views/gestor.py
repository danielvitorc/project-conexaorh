from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from ..forms import RequisicaoPessoalForm, MovimentacaoPessoalForm, RequisicaoDesligamentoForm, GestorPropostoApprovalForm
from ..models import MovimentacaoPessoal, RequisicaoPessoal

@login_required
def gestor_page(request):
    if request.user.user_type != 'gestor':
        return HttpResponseForbidden("Acesso negado! Apenas gestores podem acessar esta página.")

    form_rp = RequisicaoPessoalForm()
    form_movimentacao = MovimentacaoPessoalForm()
    form_rd = RequisicaoDesligamentoForm()
   
    movimentacao = MovimentacaoPessoal.objects.filter(
        ~Q(assinatura_complice__isnull=True),
        ~Q(assinatura_complice=""),
        gestor_proposto=request.user.username
    )
    form = GestorPropostoApprovalForm()

    if request.method == "POST":
        if "submit_rp" in request.POST:
            form_rp = RequisicaoPessoalForm(request.POST, request.FILES)
            if form_rp.is_valid():
                rp = form_rp.save(commit=False)
                rp.usuario = request.user
                rp.save()
                return redirect("gestor_page")

        elif "submit_movimentacao" in request.POST:
            form_movimentacao = MovimentacaoPessoalForm(request.POST, request.FILES)
            if form_movimentacao.is_valid():
                movimentacao = form_movimentacao.save(commit=False)
                movimentacao.save()
                return redirect("gestor_page")
        
        if "submit_aprovacao_mov" in request.POST:
            registro_id = request.POST.get("registro_id")
            if not registro_id:
                return HttpResponseBadRequest("ID do registro não informado.")
            
            registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
            form = GestorPropostoApprovalForm(request.POST, request.FILES, instance=registro)

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
            return redirect("gestor_page")
            
        elif "submit_rd" in request.POST:
            form_rd = RequisicaoDesligamentoForm(request.POST, request.FILES)
            if form_rd.is_valid():
                rd = form_rd.save(commit=False)
                rd.save()
                return redirect("gestor_page")
            

    return render(request, "conexaorh/gestor.html", {
        "form_rp": form_rp,
        "form_movimentacao": form_movimentacao,
        "form_rd": form_rd,
        "movimentacao": movimentacao,
        "form": form,
        "usuario": request.user,
    })

'''
@login_required
def registros_gestor(request):
    rp = RequisicaoPessoal.objects.filter(usuario=request.user).~Q(assinatura_rh__isnull=True), ~Q(assinatura_complice=""),
    mov 
    rd
'''