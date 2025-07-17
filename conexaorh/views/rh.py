from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponseForbidden,  JsonResponse
from django.contrib import messages
from itertools import chain
from conexaorh.forms import RHFormRP, RHFormMOV, RHFormRD, FilialForm, BaseForm, SetorForm, CursoForm, CargoForm
from conexaorh.models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento, Base, Filial, Setor, Curso, Cargo

@login_required
def rh_page(request):
    if request.user.user_type != "rh":
        return HttpResponseForbidden("Acesso negado! Apenas usuários do RH podem acessar esta página.")

    # Inicializa os formulários
    filial_form = FilialForm()
    base_form = BaseForm()
    setor_form = SetorForm()
    curso_form = CursoForm()
    cargo_form = CargoForm()

    filiais = Filial.objects.all()
    bases = Base.objects.all()
    setores = Setor.objects.all()
    cargos = Cargo.objects.all()   
    cursos = Curso.objects.all()

    # Verifica se algum formulário foi enviado
    if request.method == "POST":
        if "filial_submit" in request.POST:
            filial_form = FilialForm(request.POST)
            if filial_form.is_valid():
                filial_form.save()
                return redirect("rh_page")

        elif "base_submit" in request.POST:
            base_form = BaseForm(request.POST)
            if base_form.is_valid():
                base_form.save()
                return redirect("rh_page")

        elif "setor_submit" in request.POST:
            post_data = request.POST.copy()
            filial_id = post_data.get('filial')
            base_id = post_data.get('base')

            # Validação extra:
            if filial_id and base_id:
                if not Base.objects.filter(id=base_id, filial_id=filial_id).exists():
                    # base não pertence à filial
                    setor_form = SetorForm(post_data)
                    setor_form.add_error('base', 'Base não pertence à filial selecionada.')
                else:
                    post_data.pop('filial', None)
                    setor_form = SetorForm(post_data)
            else:
                setor_form = SetorForm(post_data)

            if setor_form.is_valid():
                setor_form.save()
                return redirect("rh_page")
            else:
                print(setor_form.errors)

        elif "curso_submit" in request.POST:
            curso_form = CursoForm(request.POST)
            if curso_form.is_valid():
                curso_form.save()
                return redirect("rh_page")

        elif "cargo_submit" in request.POST:
            post_data = request.POST.copy()
            post_data.pop('filial', None)
            post_data.pop('base', None)
            cargo_form = CargoForm(post_data)
            if cargo_form.is_valid():
                cargo_form.save()
                return redirect("rh_page")

    # Coleta os registros RP, MOV e RD
    rp = RequisicaoPessoal.objects.filter(~Q(assinatura_rh__isnull=True))
    for r in rp:
        r.tipo = "RP"

    mov = MovimentacaoPessoal.objects.filter(~Q(assinatura_rh__isnull=True))
    for m in mov:
        m.tipo = "MOV"

    rd = RequisicaoDesligamento.objects.filter(~Q(assinatura_rh__isnull=True))
    for d in rd:
        d.tipo = "RD"

    registros = sorted(chain(rp, mov, rd), key=lambda x: x.data_solicitacao, reverse=True)

    return render(request, "conexaorh/rh/rh.html", {
        "registros": registros,
        "usuario": request.user,
        "filial_form": filial_form,
        "base_form": base_form,
        "setor_form": setor_form,
        "curso_form": curso_form,
        "cargo_form": cargo_form,
        'filiais': filiais,
        "cursos": cursos,
        "cargos": cargos,
        "setores": setores,
        "bases": bases
    })


@login_required
def rh_rp(request):
    if request.user.user_type != "rh":
        return HttpResponseForbidden("Acesso negado!")

    registros = RequisicaoPessoal.objects.filter(presidente_aprovacao="AUTORIZADO").order_by('-data_solicitacao')
    form = RHFormRP()

    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = get_object_or_404(RequisicaoPessoal, id=registro_id)
        form = RHFormRP(request.POST, request.FILES, instance=registro)

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

    registros = MovimentacaoPessoal.objects.filter(presidente_aprovacao="AUTORIZADO").order_by('-data_solicitacao')
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

    registros = RequisicaoDesligamento.objects.filter(presidente_aprovacao="AUTORIZADO").order_by('-data_solicitacao')  
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


@login_required
def bases_por_filial(request):
    filial_id = request.GET.get('filial_id')
    bases = []
    if filial_id:
        bases_qs = Base.objects.filter(filial_id=filial_id).order_by('nome')
        bases = [{'id': b.id, 'nome': b.nome} for b in bases_qs]
    return JsonResponse({'bases': bases})

@login_required
def setores_por_base(request):
    base_id = request.GET.get('base_id')
    term = request.GET.get('term', '')  # termo de busca digitado pelo usuário
    setores = []

    if base_id:
        qs = Setor.objects.filter(base_id=base_id, nome__icontains=term).order_by('nome')
        setores = [{'id': s.id, 'text': s.nome} for s in qs]

    return JsonResponse({'results': setores})

def editar_filial(request, pk):
    filial = get_object_or_404(Filial, pk=pk)
    if request.method == 'POST':
        form = FilialForm(request.POST, instance=filial)
        if form.is_valid():
            form.save()
            return redirect('nome_da_sua_url_de_sucesso_filial') # Redirecione para a URL de sucesso apropriada
    else:
        form = FilialForm(instance=filial)
    return render(request, 'seu_template_de_edicao_filial.html', {'form': form, 'filial': filial})


def editar_base(request, pk):
    base = get_object_or_404(Base, pk=pk)
    if request.method == 'POST':
        form = BaseForm(request.POST, instance=base)
        if form.is_valid():
            form.save()
            return redirect('nome_da_sua_url_de_sucesso_base') # Redirecione para a URL de sucesso apropriada
    else:
        form = BaseForm(instance=base)
    return render(request, 'seu_template_de_edicao_base.html', {'form': form, 'base': base})


def editar_setor(request, pk):
    setor = get_object_or_404(Setor, pk=pk)
    if request.method == 'POST':
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            return redirect('nome_da_sua_url_de_sucesso_setor') # Redirecione para a URL de sucesso apropriada
    else:
        form = SetorForm(instance=setor)
    return render(request, 'seu_template_de_edicao_setor.html', {'form': form, 'setor': setor})


def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('nome_da_sua_url_de_sucesso_curso') # Redirecione para a URL de sucesso apropriada
    else:
        form = CursoForm(instance=curso)
    return render(request, 'seu_template_de_edicao_curso.html', {'form': form, 'curso': curso})


def editar_cargo(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('nome_da_sua_url_de_sucesso_cargo') # Redirecione para a URL de sucesso apropriada
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'seu_template_de_edicao_cargo.html', {'form': form, 'cargo': cargo})



# Função para excluir filial
def excluir_filial(request, id):
    filial = get_object_or_404(Filial, id=id)
    try:
        filial.delete()
        messages.success(request, "Filial excluída com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir a filial: {e}")
    return redirect('rh_page')  

# Função para excluir base
def excluir_base(request, id):
    base = get_object_or_404(Base, id=id)
    try:
        base.delete()
        messages.success(request, "base excluída com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir a base: {e}")
    return redirect('rh_page')  

# Função para excluir setor
def excluir_setor(request, id):
    setor = get_object_or_404(Setor, id=id)
    try:
        setor.delete()
        messages.success(request, "setor excluído com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir o setor: {e}")
    return redirect('rh_page') 

# Função para excluir curso
def excluir_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    try:
        curso.delete()
        messages.success(request, "curso excluído com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir o curso: {e}")
    return redirect('rh_page')  

# Função para excluir cargo
def excluir_cargo(request, id):
    cargo = get_object_or_404(cargo, id=id)
    try:
        cargo.delete()
        messages.success(request, "cargo excluído com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir o cargo: {e}")
    return redirect('rh_page')   