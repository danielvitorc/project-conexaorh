from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from itertools import chain
from django.db.models import Q
from conexaorh.forms import CompliceFormMOV
from conexaorh.models import MovimentacaoPessoal

@login_required
def complice_page(request):
    if request.user.user_type != 'complice':
        return HttpResponseForbidden("Acesso negado!")

    movimentacao = MovimentacaoPessoal.objects.all()

    form = CompliceFormMOV()

    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')
        if not registro_id:
            return HttpResponseBadRequest("ID do registro não informado.")
        
        registro = get_object_or_404(MovimentacaoPessoal, id=registro_id)
        form = CompliceFormMOV(request.POST, request.FILES, instance=registro)

        if form.is_valid():
            registro = form.save(commit=False)
            if registro.assinatura_complice and registro.data_autorizacao_complice is None:
                registro.data_autorizacao_complice = now()
                registro.dias_para_autorizacao_complice = (
                    registro.data_autorizacao_complice.date()
                    - registro.data_solicitacao.date()
                ).days
            form.save(user=request.user)
            return redirect('complice_page')

    return render(request, 'conexaorh/complice/complice.html', {
        'movimentacao': movimentacao,
        'usuario': request.user,
        'form': form
    })

@login_required
def registros_complice(request):
    mov = MovimentacaoPessoal.objects.filter(
        ~Q(assinatura_rh__isnull=True)
    ).select_related("usuario")
    
    return render(request, "conexaorh/complice/registros_complice.html", {
        "mov": mov,
        "usuario": request.user
    })