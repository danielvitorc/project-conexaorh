from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import RequisicaoPessoalForm, DiretorForm, PresidenteForm, RHForm, MovimentacaoPessoalForm, RequisicaoDesligamentoForm
from .models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento
from django.http import HttpResponseForbidden, HttpResponseBadRequest

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirecionamento de acordo com o tipo de usuário
            if user.user_type == 'gestor':
                return redirect('gestor_page')
            elif user.user_type == 'diretor':
                return redirect('diretor_page')
            elif user.user_type == 'presidente':
                return redirect('presidente_page')
            elif user.user_type == 'rh':
                return redirect('rh_page')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'conexaorh/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def gestor_page(request):
    if request.user.user_type != 'gestor':
        return HttpResponseForbidden("Acesso negado! Apenas gestores podem acessar esta página.")

    form_rp = RequisicaoPessoalForm()
    form_movimentacao = MovimentacaoPessoalForm()
    form_rd = RequisicaoDesligamentoForm()

    if request.method == "POST":
        if "submit_rp" in request.POST:
            form_rp = RequisicaoPessoalForm(request.POST)
            if form_rp.is_valid():
                rp = form_rp.save(commit=False)
                rp.gestor = request.user
                rp.save()
                return redirect("gestor_page")

        elif "submit_movimentacao" in request.POST:
            form_movimentacao = MovimentacaoPessoalForm(request.POST)
            if form_movimentacao.is_valid():
                movimentacao = form_movimentacao.save(commit=False)
                movimentacao.save()
                return redirect("gestor_page")
            
        elif "submit_rd" in request.POST:
            form_rd = RequisicaoDesligamentoForm(request.POST)
            if form_rd.is_valid():
                rd = form_rd.save(commit=False)
                rd.save()
                return redirect("gestor_page")

    return render(request, "conexaorh/gestor.html", {
        "form_rp": form_rp,
        "form_movimentacao": form_movimentacao,
        "form_rd": form_rd,
         "usuario": request.user,
    })


@login_required
def diretor_page(request):
    if request.user.user_type != "diretor":
        return HttpResponseForbidden("Acesso negado! Apenas diretores podem acessar esta página.")

    rp = RequisicaoPessoal.objects.all()
    movimentacao = MovimentacaoPessoal.objects.all()
    rd = RequisicaoDesligamento.objects.all()

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

        form = DiretorForm(request.POST, instance=registro)

        if form.is_valid():
            novo_status = form.cleaned_data["status_diretor"]

            if novo_status == "aprovado":  
                if registro.data_autorizacao_diretor is None:
                    registro.data_autorizacao_diretor = now()

                diferenca_dias = (registro.data_autorizacao_diretor.date() - registro.data_solicitacao.date()).days
                registro.dias_para_autorizacao_diretor = max(0, diferenca_dias)  

            registro.status_diretor = novo_status
            registro.save()
            
            return redirect("diretor_page")

    return render(request, "conexaorh/diretor.html", {"rp": rp, "movimentacao": movimentacao, "rd": rd, "usuario": request.user})


@login_required
def presidente_page(request):
    if request.user.user_type != "presidente":
        return HttpResponseForbidden("Acesso negado! Apenas presidentes podem acessar esta página.")

    rp = RequisicaoPessoal.objects.filter(status_diretor="aprovado")
    movimentacao = MovimentacaoPessoal.objects.filter(status_diretor="aprovado")
    rd = RequisicaoDesligamento.objects.filter(status_diretor="aprovado")

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

        form = PresidenteForm(request.POST, instance=registro)

        if form.is_valid():
            novo_status = form.cleaned_data["status_presidente"]

            if novo_status == "aprovado":  
                if registro.data_autorizacao_presidente is None:
                    registro.data_autorizacao_presidente = now()

                if registro.data_autorizacao_diretor:
                    diferenca_dias = (registro.data_autorizacao_presidente.date() - registro.data_autorizacao_diretor.date()).days
                    registro.dias_para_autorizacao_presidente = max(0, diferenca_dias)

            registro.status_presidente = novo_status
            registro.save()
            
            return redirect("presidente_page")

    return render(
        request, 
        "conexaorh/presidente.html", 
        {"rp": rp, "movimentacao": movimentacao, "rd": rd, "usuario": request.user,}
    )

@login_required
def rh_page(request):
    if request.user.user_type != "rh":
        return HttpResponseForbidden("Acesso negado! Apenas usuários do RH podem acessar esta página.")

    # Buscar registros dos dois modelos que já foram aprovados pelo presidente
    rp = RequisicaoPessoal.objects.filter(status_presidente="aprovado")
    movimentacao = MovimentacaoPessoal.objects.filter(status_presidente="aprovado")
    rd = RequisicaoDesligamento.objects.filter(status_presidente="aprovado")

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

        form = RHForm(request.POST, instance=registro)

        if form.is_valid():
            novo_status = form.cleaned_data["status_rh"]

            if novo_status == "aprovado":
                if registro.data_autorizacao_rh is None:
                    registro.data_autorizacao_rh = now()

                if registro.data_autorizacao_presidente:
                    diferenca_dias = (registro.data_autorizacao_rh.date() - registro.data_autorizacao_presidente.date()).days
                    registro.dias_para_autorizacao_rh = max(0, diferenca_dias)

            registro.status_rh = novo_status
            registro.save()

            return redirect("rh_page")

    return render(
        request,
        "conexaorh/rh.html",
        {"rp": rp, "movimentacao": movimentacao, "rd": rd, "usuario": request.user,}
    )



