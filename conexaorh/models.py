from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
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

HASH_ASSINATURAS_DIRETORES = [
    "ec13c29d7a2838322cca4d38262954072e9282ff63daa09874f2fc89ab100497"
 ]

HASHES_ASSINATURAS_PRESIDENTE = [
    "c101cac72891d0d1586d0791a028ef2adcdcc3a7cbd53caec4c2bda8f8a443c0"
]
HASHES_ASSINATURAS_RH = [
    "8e551767cfe9d662f0185cff3840c4616401a3726f52898ee38857cf495cbb8f"
]  
HASHES_ASSINATURAS_COMPLICE = [
    "bc61c2c356167b859d9a008035e841ee32236ad44356772bfd5cec4cde5b3ffc"
]
HASHES_ASSINATURAS_GESTORES = [
    "ec8ff0a6954a5f54e4ad246f0a788d076f675e457bca16a04248718cca3fe631"
]

class RequisicaoPessoal(models.Model):
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    justificativa_outros = models.CharField(max_length=100, null=True, blank=True)
    processo_seletivo = models.CharField(max_length=100)
    localidade = models.CharField(max_length=100, default="MANAUS", )
    base = models.CharField(max_length=100 ,default="N/A", )
    sexo = models.CharField(max_length=100)
    exige_viagem = models.CharField(max_length=100)
    cnh = models.CharField(max_length=100)
    tipo_cnh = models.CharField(max_length=100)
    outros_cnh = models.CharField(max_length=100, null=True, blank=True)
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


    # Assinatura do Gestor
    assinatura_gestor = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_assinadas_como_gestor')
    data_autorizacao_gestor = models.DateTimeField(null=True, blank=True, auto_now_add=True)    
    imagem_assinatura_gestor = models.ImageField(upload_to="assinaturas/gestor/RequisicaoPessoal", null=True, blank=True)

    # Assinatura do Diretor
    assinatura_diretor = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_assinadas_como_diretor')
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/RequisicaoPessoal", null=True, blank=True)

    # Assinatura do presidente
    assinatura_presidente = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_assinadas_como_presidente')
    data_autorizacao_presidente = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_presidente = models.ImageField(upload_to="assinaturas/presidente/RequisicaoPessoal", null=True, blank=True)

    # Assinatura do RH
    assinatura_rh = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_assinadas_como_rh')
    data_autorizacao_rh = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_rh = models.ImageField(upload_to="assinaturas/rh/RequisicaoPessoal", null=True, blank=True)

    dias_para_autorizacao_diretor = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_presidente = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_rh = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Requisição {self.n_rp or 'Sem número'}"
    

    def assinar_gestor(self, user):
        self.assinatura_gestor = user
        self.data_assinatura_gestor = timezone.now()
        self.save()

    def assinar_diretor(self, user):
        self.assinatura_diretor = user
        self.data_assinatura_diretor = timezone.now()
        self.save()

    def assinar_presidente(self, user):
        self.assinatura_presidente = user
        self.data_assinatura_presidente = timezone.now()
        self.save()

    def assinar_rh(self, user):
        self.assinatura_rh = user
        self.data_assinatura_rh = timezone.now()
        self.save()



class MovimentacaoPessoal(models.Model):
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    n_mov =  models.PositiveIntegerField(unique=True, editable=False, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.n_mov:
            ultimo = MovimentacaoPessoal.objects.aggregate(maior=models.Max('n_mov'))['maior']
            if ultimo is None:
                self.n_mov = 1
            else:                       
                self.n_mov = ultimo + 1   
        super().save(*args, **kwargs)

    unidade = models.CharField(max_length=100, default="MANAUS")
    tipo_movimentacao = models.CharField(max_length=255)
    outro_tipo = models.CharField(max_length=100, null=True, blank=True)
    colaborador_movimentado = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)
    data_admissao = models.DateField()
    outro_info = models.CharField(max_length=100, null=True, blank=True)
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
    tipo_ajuda_custo = models.CharField(max_length=100, null=True, blank=True)
    valor_ajuda = models.FloatField(null=True, blank=True)
    periodo =  models.CharField(max_length=100)
    jutificativa_movimentacao = models.CharField(max_length=100)
    outro_justificativa = models.CharField(max_length=100, null=True, blank=True)
    substituicao = models.CharField(max_length=100)
    comentarios = models.TextField()

    assinatura_gestor_atual =  models.ImageField(upload_to="assinaturas/gestor/MovimentacaoPessoal/", null=True, blank=True)
    data_autorizacao_gestor_atual = models.DateTimeField(null=True, blank=True, auto_now_add=True)

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

    def __str__(self):
        return f"Movimentação: {self.colaborador_movimentado} ({self.tipo_movimentacao}) - {self.data_solicitacao.strftime('%d/%m/%Y')}"
    
    def clean(self):
        super().clean()

     # Validação da assinatura do Gestor Atual
        if self.assinatura_gestor_atual and hasattr(self.assinatura_gestor_atual, 'file'):
            try:
                self.assinatura_gestor_atual.seek(0)
                hash_gestor_atual = hashlib.sha256(self.assinatura_gestor_atual.file.read()).hexdigest()
                self.assinatura_gestor_atual.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do gestor atual")
    
            if hash_gestor_atual not in HASHES_ASSINATURAS_GESTORES:
                raise ValidationError({"assinatura_gestor_atual": "Arquivo de assinatura do Gestor Atual inválido."})

     # Validação da assinatura do Complice
        if self.assinatura_complice and hasattr(self.assinatura_complice, 'file'):
            try:
                self.assinatura_complice.seek(0)
                hash_complice = hashlib.sha256(self.assinatura_complice.file.read()).hexdigest()
                self.assinatura_complice.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do Complice.")
    
            if hash_complice not in HASHES_ASSINATURAS_COMPLICE:
                raise ValidationError({"assinatura_complice": "Arquivo de assinatura do Complice inválido."})
             
     # Validação da assinatura do Gestor Proposto
        if self.assinatura_gestor_proposto and hasattr(self.assinatura_gestor_proposto, 'file'):
            try:
                self.assinatura_gestor_proposto.seek(0)
                hash_gestor= hashlib.sha256(self.assinatura_gestor_proposto.read()).hexdigest()
                self.assinatura_gestor_proposto.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do Gestor Proposto")
            
            if hash_gestor not in HASHES_ASSINATURAS_GESTORES:
                 raise ValidationError({"assinatura_gestor_proposto": "Arquivo de assinatura do Gestor Proposto inválido."})
            
     # Validação da assinatura do diretor
        if self.assinatura_diretor and hasattr(self.assinatura_diretor, 'file'):
            try:
                self.assinatura_diretor.file.seek(0)
                hash_diretor = hashlib.sha256(self.assinatura_diretor.file.read()).hexdigest()
                self.assinatura_diretor.file.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do diretor.")
            
            if hash_diretor not in HASH_ASSINATURAS_DIRETORES:
                raise ValidationError("Arquivo de assinatura do diretor inválido.")

    # Validação da assinatura do presidente
        if self.assinatura_presidente and hasattr(self.assinatura_presidente, 'file'):
            try:
                self.assinatura_presidente.file.seek(0)
                hash_presidente = hashlib.sha256(self.assinatura_presidente.file.read()).hexdigest()
                self.assinatura_presidente.file.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do presidente.")
            
            if hash_presidente not in HASHES_ASSINATURAS_PRESIDENTE:
                raise ValidationError("Arquivo de assinatura do presidente inválido.")
            
     # Validação da assinatura do RH       
        if self.assinatura_rh and hasattr(self.assinatura_rh, 'file'):
            try:
                self.assinatura_rh.file.seek(0)
                hash_rh = hashlib.sha256(self.assinatura_rh.file.read()).hexdigest()
                self.assinatura_rh.file.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do rh.")
            
            if hash_rh not in HASHES_ASSINATURAS_RH:
                raise ValidationError("Arquivo de assinatura do rh inválido.")

    
    
class RequisicaoDesligamento(models.Model):
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requisitante = models.CharField(max_length=100)
    colaborador_desligado = models.CharField(max_length=100)
    data_desligamento = models.DateField()
    funcao = models.CharField(max_length=100)
    salario = models.FloatField()
    localidade = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)
    data_admissao = models.DateField()
    centro_custo = models.CharField(max_length=100)
    tipo_desligamento = models.CharField(max_length=200)
    motivo_desligamento = models.CharField(max_length=200)
    outro_motivo = models.CharField(max_length=100, null=True, blank=True)
    justificativa_desligamento = models.TextField()
    tipo_aviso = models.CharField(max_length=100)
    justificativa_aviso = models.TextField()
    substituicao = models.CharField(max_length=100)
    bloqueio_readmissao = models.BooleanField(default=False)

    
    # Assinatura do Gestor
    assinatura_gestor = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_desligamento_como_gestor')
    data_autorizacao_gestor = models.DateTimeField(null=True, blank=True, auto_now_add=True)    
    imagem_assinatura_gestor = models.ImageField(upload_to="assinaturas/gestor/RequisicaoDesligamento", null=True, blank=True)

    # Assinatura do Diretor
    assinatura_diretor = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_desligamento_como_diretor')
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/RequisicaoDesligamento", null=True, blank=True)

    # Assinatura do presidente
    assinatura_presidente = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_desligamento_como_presidente')
    data_autorizacao_presidente = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_presidente = models.ImageField(upload_to="assinaturas/presidente/RequisicaoDesligamento", null=True, blank=True)

    # Assinatura do RH
    assinatura_rh = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_desligamento_como_rh')
    data_autorizacao_rh = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_rh = models.ImageField(upload_to="assinaturas/rh/RequisicaoDesligamento", null=True, blank=True)

    dias_para_autorizacao_diretor = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_presidente = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_rh = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Requisição {self.n_rp or 'Sem número'}"
    

    def assinar_gestor(self, user):
        self.assinatura_gestor = user
        self.data_assinatura_gestor = timezone.now()
        self.save()

    def assinar_diretor(self, user):
        self.assinatura_diretor = user
        self.data_assinatura_diretor = timezone.now()
        self.save()

    def assinar_presidente(self, user):
        self.assinatura_presidente = user
        self.data_assinatura_presidente = timezone.now()
        self.save()

    def assinar_rh(self, user):
        self.assinatura_rh = user
        self.data_assinatura_rh = timezone.now()
        self.save()
