from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponseForbidden,  JsonResponse
from itertools import chain
from conexaorh.forms import RHFormRP, RHFormMOV, RHFormRD, FilialForm, BaseForm, SetorForm, CursoForm, CargoForm
from conexaorh.models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento, Base, Filial, Setor, Curso

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
        "cursos": cursos
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
