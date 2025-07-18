from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from itertools import chain
from conexaorh.forms import RHFormRP, RHFormMOV, RHFormRD, FilialForm, BaseForm, SetorForm, CursoForm, CargoForm
from conexaorh.models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento, Base, Filial, Setor, Curso, Cargo

# Configurar logging para debug
logger = logging.getLogger(__name__)

def is_ajax_request(request):
    """Verifica se é uma requisição AJAX de forma mais robusta"""
    return (
        request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
        request.headers.get('Content-Type') == 'application/json' or
        'ajax' in request.GET or
        'ajax' in request.POST
    )

def ajax_response(success=True, message='', data=None, errors=None):
    """Função helper para garantir respostas JSON consistentes"""
    response_data = {
        'success': success,
        'message': message
    }
    
    if data:
        response_data.update(data)
    
    if errors:
        response_data['errors'] = errors
    
    return JsonResponse(response_data)

@login_required
def rh_page(request):
    if request.user.user_type != "rh":
        return HttpResponseForbidden("Acesso negado! Apenas usuários do RH podem acessar esta página.")

    # Verifica se é AJAX logo no início
    is_ajax = is_ajax_request(request)
    
    # Log para debug
    if is_ajax:
        logger.info(f"Requisição AJAX detectada. POST data: {dict(request.POST)}")

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
        try:
            # Log dos dados POST para debug
            logger.info(f"POST data recebido: {dict(request.POST)}")
            
            # Verifica qual botão foi pressionado
            submit_buttons = [key for key in request.POST.keys() if key.endswith('_submit')]
            logger.info(f"Botões de submit encontrados: {submit_buttons}")
            
            if "filial_submit" in request.POST:
                logger.info("Processando formulário de filial")
                filial_form = FilialForm(request.POST)
                if filial_form.is_valid():
                    filial = filial_form.save()
                    if is_ajax:
                        return ajax_response(
                            success=True,
                            message='Filial cadastrada com sucesso!',
                            data={
                                'filial': {
                                    'id': filial.id,
                                    'nome': filial.nome
                                }
                            }
                        )
                    messages.success(request, 'Filial cadastrada com sucesso!')
                    return redirect("rh_page")
                else:
                    logger.error(f"Erro na validação do formulário de filial: {filial_form.errors}")
                    if is_ajax:
                        return ajax_response(
                            success=False,
                            message='Erro ao cadastrar filial',
                            errors=filial_form.errors
                        )

            elif "base_submit" in request.POST:
                logger.info("Processando formulário de base")
                base_form = BaseForm(request.POST)
                if base_form.is_valid():
                    base = base_form.save()
                    if is_ajax:
                        return ajax_response(
                            success=True,
                            message='Base cadastrada com sucesso!',
                            data={
                                'base': {
                                    'id': base.id,
                                    'nome': base.nome,
                                    'filial': base.filial.nome
                                }
                            }
                        )
                    messages.success(request, 'Base cadastrada com sucesso!')
                    return redirect("rh_page")
                else:
                    logger.error(f"Erro na validação do formulário de base: {base_form.errors}")
                    if is_ajax:
                        return ajax_response(
                            success=False,
                            message='Erro ao cadastrar base',
                            errors=base_form.errors
                        )

            elif "setor_submit" in request.POST:
                logger.info("Processando formulário de setor")
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
                    setor = setor_form.save()
                    if is_ajax:
                        return ajax_response(
                            success=True,
                            message='Setor cadastrado com sucesso!',
                            data={
                                'setor': {
                                    'id': setor.id,
                                    'centro_de_custo': setor.centro_de_custo,
                                    'nome': setor.nome,
                                    'base': setor.base.nome
                                }
                            }
                        )
                    messages.success(request, 'Setor cadastrado com sucesso!')
                    return redirect("rh_page")
                else:
                    logger.error(f"Erro na validação do formulário de setor: {setor_form.errors}")
                    if is_ajax:
                        return ajax_response(
                            success=False,
                            message='Erro ao cadastrar setor',
                            errors=setor_form.errors
                        )

            elif "curso_submit" in request.POST:
                logger.info("Processando formulário de curso")
                curso_form = CursoForm(request.POST)
                if curso_form.is_valid():
                    curso = curso_form.save()
                    if is_ajax:
                        return ajax_response(
                            success=True,
                            message='Curso cadastrado com sucesso!',
                            data={
                                'curso': {
                                    'id': curso.id,
                                    'nome': curso.nome
                                }
                            }
                        )
                    messages.success(request, 'Curso cadastrado com sucesso!')
                    return redirect("rh_page")
                else:
                    logger.error(f"Erro na validação do formulário de curso: {curso_form.errors}")
                    if is_ajax:
                        return ajax_response(
                            success=False,
                            message='Erro ao cadastrar curso',
                            errors=curso_form.errors
                        )

            elif "cargo_submit" in request.POST:
                logger.info("Processando formulário de cargo")
                post_data = request.POST.copy()
                post_data.pop('filial', None)
                post_data.pop('base', None)
                cargo_form = CargoForm(post_data)
                if cargo_form.is_valid():
                    cargo = cargo_form.save()
                    if is_ajax:
                        return ajax_response(
                            success=True,
                            message='Cargo cadastrado com sucesso!',
                            data={
                                'cargo': {
                                    'id': cargo.id,
                                    'nome': cargo.nome
                                }
                            }
                        )
                    messages.success(request, 'Cargo cadastrado com sucesso!')
                    return redirect("rh_page")
                else:
                    logger.error(f"Erro na validação do formulário de cargo: {cargo_form.errors}")
                    if is_ajax:
                        return ajax_response(
                            success=False,
                            message='Erro ao cadastrar cargo',
                            errors=cargo_form.errors
                        )
            
            # Se chegou até aqui e é AJAX, significa que não encontrou nenhum submit válido
            if is_ajax:
                logger.warning(f"Nenhum submit válido encontrado para requisição AJAX. POST keys: {list(request.POST.keys())}")
                return ajax_response(
                    success=False,
                    message='Nenhuma ação válida encontrada',
                    errors={'__all__': [f'Formulário não identificado. Botões encontrados: {submit_buttons}']}
                )
                        
        except Exception as e:
            # Em caso de erro inesperado, SEMPRE retorna JSON para AJAX
            logger.error(f"Erro inesperado no processamento: {str(e)}", exc_info=True)
            if is_ajax:
                return ajax_response(
                    success=False,
                    message='Erro interno do servidor',
                    errors={'__all__': [f'Erro interno: {str(e)}']}
                )
            # Para requisições normais, adiciona mensagem de erro e continua
            messages.error(request, f'Ocorreu um erro: {str(e)}')

    # Se chegou até aqui e é uma requisição AJAX POST sem ação válida
    if request.method == "POST" and is_ajax:
        logger.warning("Requisição AJAX POST sem ação válida identificada")
        return ajax_response(
            success=False,
            message='Requisição inválida',
            errors={'__all__': ['Nenhuma ação válida foi encontrada']}
        )

    # Coleta os registros RP, MOV e RD
    try:
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
    except Exception as e:
        registros = []
        logger.error(f"Erro ao carregar registros: {str(e)}")
        if is_ajax:
            return ajax_response(
                success=False,
                message='Erro ao carregar registros',
                errors={'__all__': [f'Erro ao carregar dados: {str(e)}']}
            )

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








# Sua função helper para respostas de erro em JSON
def json_response(success, message, errors=None, status=200 ):
    data = {'success': success, 'message': message}
    if errors:
        data['errors'] = errors
    return JsonResponse(data, status=status)

@login_required
@require_http_methods(["POST"] )
def editar_filial(request, pk):
    filial = get_object_or_404(Filial, pk=pk)
    form = FilialForm(request.POST, instance=filial)
    if form.is_valid():
        form.save()
        # Redireciona para a página 'rh_page' em caso de sucesso
        return redirect('rh_page')
    else:
        return json_response(False, 'Erro de validação.', errors=form.errors, status=400)

@login_required
@require_http_methods(["POST"] )
def editar_base(request, pk):
    base = get_object_or_404(Base, pk=pk)
    form = BaseForm(request.POST, instance=base)
    if form.is_valid():
        form.save()
        # Redireciona para a página 'rh_page' em caso de sucesso
        return redirect('rh_page')
    else:
        return json_response(False, 'Erro de validação.', errors=form.errors, status=400)

@login_required
@require_http_methods(["POST"] )
def editar_setor(request, pk):
    setor = get_object_or_404(Setor, pk=pk)
    form = SetorForm(request.POST, instance=setor)
    if form.is_valid():
        form.save()
        # Redireciona para a página 'rh_page' em caso de sucesso
        return redirect('rh_page')
    else:
        return json_response(False, 'Erro de validação.', errors=form.errors, status=400)

@login_required
@require_http_methods(["POST"] )
def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    form = CursoForm(request.POST, instance=curso)
    if form.is_valid():
        form.save()
        # Redireciona para a página 'rh_page' em caso de sucesso
        return redirect('rh_page')
    else:
        return json_response(False, 'Erro de validação.', errors=form.errors, status=400)

@login_required
@require_http_methods(["POST"] )
def editar_cargo(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    form = CargoForm(request.POST, instance=cargo)
    if form.is_valid():
        form.save()
        # Redireciona para a página 'rh_page' em caso de sucesso
        return redirect('rh_page')
    else:
        return json_response(False, 'Erro de validação.', errors=form.errors, status=400)

# --- Funções de Exclusão (sem alterações, já estão corretas) ---

@login_required
def excluir_filial(request, id):
    filial = get_object_or_404(Filial, id=id)
    try:
        filial.delete()
        messages.success(request, "Filial excluída com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir a filial: {e}")
    return redirect('rh_page')  

@login_required
def excluir_base(request, id):
    base = get_object_or_404(Base, id=id)
    try:
        base.delete()
        messages.success(request, "Base excluída com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir a base: {e}")
    return redirect('rh_page')  

@login_required
def excluir_setor(request, id):
    setor = get_object_or_404(Setor, id=id)
    try:
        setor.delete()
        messages.success(request, "Setor excluído com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir o setor: {e}")
    return redirect('rh_page') 

@login_required
def excluir_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    try:
        curso.delete()
        messages.success(request, "Curso excluído com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir o curso: {e}")
    return redirect('rh_page')  

@login_required
def excluir_cargo(request, id):
    cargo = get_object_or_404(Cargo, id=id)
    try:
        cargo.delete()
        messages.success(request, "Cargo excluído com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir o cargo: {e}")
    return redirect('rh_page')