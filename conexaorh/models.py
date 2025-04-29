from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
import hashlib
from django.contrib.auth import get_user_model
from django.db.models import Max

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('gestor', 'Gestor'),
        ('diretor', 'Diretor'),
        ('presidente', 'Presidente'),
        ('rh', 'RH'),
        ('complice','Complice')
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

User = get_user_model()

HASH_ASSINATURAS_DIRETORES = "ec13c29d7a2838322cca4d38262954072e9282ff63daa09874f2fc89ab100497"
HASHES_ASSINATURAS_PRESIDENTE = "ec13c29d7a2838322cca4d38262954072e9282ff63daa09874f2fc89ab100497"
HASHES_ASSINATURAS_RH = "ec13c29d7a2838322cca4d38262954072e9282ff63daa09874f2fc89ab100497"  
HASHES_ASSINATURAS_COMPLICE = "ec13c29d7a2838322cca4d38262954072e9282ff63daa09874f2fc89ab100497"
HASHES_ASSINATURAS_GESTORES = "ec13c29d7a2838322cca4d38262954072e9282ff63daa09874f2fc89ab100497"

class RequisicaoPessoal(models.Model):
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    requisitante= models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    salario = models.FloatField()
    adicionais = models.FloatField(default=0)
    quantidade_vagas = models.IntegerField()
    horario_trabalho_inicio = models.TimeField()
    horario_trabalho_fim = models.TimeField()
    tipo_ponto = models.CharField(max_length=100)
    inicio_contrato = models.DateField()
    termino_contrato = models.DateField()
    tipo_contratacao = models.CharField(max_length=100)
    motivo_contracao = models.CharField(max_length=100)
    beneficios = models.CharField(max_length=100)
    subtituicao = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)
    justificativa_substituicao = models.CharField(max_length=100)
    justificativa_outros = models.CharField(max_length=100)
    processo_seletivo = models.CharField(max_length=100)
    localidade = models.CharField(max_length=100, default="MANAUS", )
    base = models.CharField(max_length=100 ,default="N/A", )
    sexo = models.CharField(max_length=100)
    exige_viagem = models.CharField(max_length=100)
    cnh = models.CharField(max_length=100)
    tipo_cnh = models.CharField(max_length=100)
    outros_cnh = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    escolaridade = models.CharField(max_length=100, default="ENSINO MÉDIO COMPLETO", )
    gestor_imediato = models.CharField(max_length=100)
    centro_custo = models.CharField(max_length=100)
    cursos = models.TextField()
    experiencias = models.TextField()
    habilidades_comportamentais = models.TextField(default="ADAPTAÇÃO E FLEXIBILIDADE COMUNICAÇÃO ATENÇÃO CONCENTRADA ÉTICA")
    principais_atribuicoes = models.TextField()
    candidato_aprovado = models.CharField(max_length=100)
    n_rp = models.PositiveIntegerField(unique=True, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.n_rp:
            ultimo = RequisicaoPessoal.objects.aggregate(maior=models.Max('n_rp'))['maior']
            if ultimo is None:
                self.n_rp = 1
            else:
                self.n_rp = ultimo + 1
        super().save(*args, **kwargs)

    # Assinatura do diretor
    assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/RequisicaoPessoal")
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)

    # Assinatura do presidente
    assinatura_presidente = models.ImageField(upload_to="assinaturas/presidente/RequisicaoPessoal")
    data_autorizacao_presidente = models.DateTimeField(null=True, blank=True)

    # Assinatura do RH
    assinatura_rh = models.ImageField(upload_to="assinaturas/rh/RequisicaoPessoal")
    data_autorizacao_rh = models.DateTimeField(null=True, blank=True)

    dias_para_autorizacao_diretor = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_presidente = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_rh = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome_colaborador} - Diretor: {self.get_status_diretor_display()} - Presidente: {self.get_status_presidente_display()} - RH: {self.get_status_rh_display()}"
    
    def clean(self):
        super().clean()

     # Validação da assinatura do diretor
        if self.assinatura_diretor:
             hash_recebido = hashlib.sha256(self.assinatura_diretor.read()).hexdigest()
             self.assinatura_diretor.seek(0)
             if hash_recebido != HASH_ASSINATURAS_DIRETORES:
                 raise ValidationError({"assinatura_diretor": "Arquivo Inválido."})

    # Validação da assinatura do presidente
        if self.assinatura_presidente:
            hash_presidente = hashlib.sha256(self.assinatura_presidente.read()).hexdigest()
            self.assinatura_presidente.seek(0)
            if hash_presidente not in HASHES_ASSINATURAS_PRESIDENTE:
                raise ValidationError({"assinatura_presidente": "Arquivo de assinatura do presidente inválido."})
     # Validação da assinatura do RH       
        if self.assinatura_rh:
            hash_rh = hashlib.sha256(self.assinatura_rh.read()).hexdigest()
            self.assinatura_rh.seek(0)
            if hash_rh not in HASHES_ASSINATURAS_RH:
                raise ValidationError({"assinatura_rh": "Arquivo de assinatura do RH inválido."})
    
class MovimentacaoPessoal(models.Model):
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    numero = models.CharField(max_length=100)
    unidade = models.CharField(max_length=100, default="MANAUS")
    tipo_movimentacao = models.CharField(max_length=100)
    outro_tipo = models.CharField(max_length=100)
    colaborador_movimentado = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)
    data_admissao = models.DateField()
    outro_info = models.CharField(max_length=100)
    localidade_atual = models.CharField(max_length=100)
    cargo_atual = models.CharField(max_length=100)
    departamento_atual = models.CharField(max_length=100)
    salario_atual = models.FloatField()
    gestor_atual = models.CharField(max_length=100)
    centro_custo_atual = models.CharField(max_length=100)
    localidade_proposta = models.CharField(max_length=100)
    cargo_proposto = models.CharField(max_length=100)
    departamento_proposto = models.CharField(max_length=100)
    salario_proposto = models.FloatField()
    gestor_proposto = models.CharField(max_length=100)
    centro_custo_proposto = models.CharField(max_length=100)
    data_movimentacao = models.DateField()
    tipo_adicional = models.CharField(max_length=100)
    tipo_ajuda_custo = models.CharField(max_length=100)
    valor_ajuda = models.FloatField()
    periodo =  models.CharField(max_length=100)
    jutificativa_movimentacao = models.CharField(max_length=100)
    outro_justificativa = models.CharField(max_length=100)
    substituicao = models.CharField(max_length=100)
    comentarios = models.TextField()

    assinatura_complice = models.ImageField(upload_to="assinaturas/complice/MovimentacaoPessoal/")
    data_autorizacao_complice = models.DateTimeField(null=True, blank=True)
    dias_para_autorizacao_complice = models.IntegerField(null=True, blank=True)

    assinatura_gestor_proposto = models.ImageField(upload_to="assinaturas/gestor/MovimentacaoPessoal/")
    data_autorizacao_gestor_proposto = models.DateTimeField(null=True, blank=True)
    dias_para_autorizacao_gestor_proposto = models.IntegerField(null=True, blank=True)

    assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/MovimentacaoPessoal/")
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)
    dias_para_autorizacao_diretor = models.IntegerField(null=True, blank=True)

    assinatura_presidente = models.ImageField(upload_to="assinaturas/presidente/MovimentacaoPessoal/")
    data_autorizacao_presidente = models.DateTimeField(null=True, blank=True)
    dias_para_autorizacao_presidente = models.IntegerField(null=True, blank=True)

    assinatura_rh = models.ImageField(upload_to="assinaturas/rh/MovimentacaoPessoal/", null=True, blank=True)
    data_autorizacao_rh = models.DateTimeField(null=True, blank=True)
    dias_para_autorizacao_rh = models.IntegerField(null=True, blank=True)

    def clean(self):
        super().clean()

     # Validação da assinatura do Complice
        if self.assinatura_complice:
             hash_recebido = hashlib.sha256(self.assinatura_complice.read()).hexdigest()
             self.assinatura_complice.seek(0)
             if hash_recebido != HASHES_ASSINATURAS_COMPLICE:
                 raise ValidationError({"assinatura_complice": "Arquivo de assinatura do Complice inválido."})
             
     # Validação da assinatura do Gestor Proposto
        if self.assinatura_gestor_proposto:
             hash_recebido = hashlib.sha256(self.assinatura_gestor_proposto.read()).hexdigest()
             self.assinatura_gestor_proposto.seek(0)
             if hash_recebido != HASHES_ASSINATURAS_GESTORES:
                 raise ValidationError({"assinatura_gestor_proposto": "Arquivo de assinatura do Gestor Proposto inválido."})
     # Validação da assinatura do diretor
        if self.assinatura_diretor:
             hash_recebido = hashlib.sha256(self.assinatura_diretor.read()).hexdigest()
             self.assinatura_diretor.seek(0)
             if hash_recebido != HASH_ASSINATURAS_DIRETORES:
                 raise ValidationError({"assinatura_diretor": "Arquivo Inválido."})

    # Validação da assinatura do presidente
        if self.assinatura_presidente:
            hash_presidente = hashlib.sha256(self.assinatura_presidente.read()).hexdigest()
            self.assinatura_presidente.seek(0)
            if hash_presidente not in HASHES_ASSINATURAS_PRESIDENTE:
                raise ValidationError({"assinatura_presidente": "Arquivo de assinatura do presidente inválido."})
     # Validação da assinatura do RH       
        if self.assinatura_rh:
            hash_rh = hashlib.sha256(self.assinatura_rh.read()).hexdigest()
            self.assinatura_rh.seek(0)
            if hash_rh not in HASHES_ASSINATURAS_RH:
                raise ValidationError({"assinatura_rh": "Arquivo de assinatura do RH inválido."})

    
    
class RequisicaoDesligamento(models.Model):
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    requisitante = models.CharField(max_length=100)
    colaborador_desligado = models.CharField(max_length=100)
    data_desligamento = models.DateField()
    funcao = models.CharField(max_length=100)
    salario = models.FloatField()
    localidade = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)
    data_admissao = models.DateField()
    centro_custo = models.CharField(max_length=100)
    tipo_desligamento = models.CharField(max_length=100)
    motivo_desligamento = models.CharField(max_length=100)
    outro_motivo = models.CharField(max_length=100)
    justificativa_desligamento = models.TextField()
    tipo_aviso = models.CharField(max_length=100)
    justificativa_aviso = models.TextField()
    substituicao = models.CharField(max_length=100)


    assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/RequisicaoDesligamento/")
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)
    dias_para_autorizacao_diretor = models.IntegerField(null=True, blank=True)

    assinatura_presidente = models.ImageField(upload_to="assinaturas/presidente/RequisicaoDesligamento/")
    data_autorizacao_presidente = models.DateTimeField(null=True, blank=True)
    dias_para_autorizacao_presidente = models.IntegerField(null=True, blank=True)

    assinatura_rh = models.ImageField(upload_to="assinaturas/rh/RequisicaoDesligamento/")
    data_autorizacao_rh = models.DateTimeField(null=True, blank=True)
    dias_para_autorizacao_rh = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Registro por {self.titulo} ({self.cargo}) - {self.data_criacao.strftime('%d/%m/%Y')}"

    def clean(self):
        super().clean()

     # Validação da assinatura do diretor
        if self.assinatura_diretor:
             hash_recebido = hashlib.sha256(self.assinatura_diretor.read()).hexdigest()
             self.assinatura_diretor.seek(0)
             if hash_recebido != HASH_ASSINATURAS_DIRETORES:
                 raise ValidationError({"assinatura_diretor": "Arquivo Inválido."})

    # Validação da assinatura do presidente
        if self.assinatura_presidente:
            hash_presidente = hashlib.sha256(self.assinatura_presidente.read()).hexdigest()
            self.assinatura_presidente.seek(0)
            if hash_presidente not in HASHES_ASSINATURAS_PRESIDENTE:
                raise ValidationError({"assinatura_presidente": "Arquivo de assinatura do presidente inválido."})
     # Validação da assinatura do RH       
        if self.assinatura_rh:
            hash_rh = hashlib.sha256(self.assinatura_rh.read()).hexdigest()
            self.assinatura_rh.seek(0)
            if hash_rh not in HASHES_ASSINATURAS_RH:
                raise ValidationError({"assinatura_rh": "Arquivo de assinatura do RH inválido."})