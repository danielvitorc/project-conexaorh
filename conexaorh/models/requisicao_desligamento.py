from django.conf import settings
from .users import CustomUser as User
from django.db import models
from django.utils import timezone

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
    diretor_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
    assinatura_diretor = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_desligamento_como_diretor')
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/RequisicaoDesligamento", null=True, blank=True)

    # Assinatura do presidente
    presidente_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
    assinatura_presidente = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_desligamento_como_presidente')
    data_autorizacao_presidente = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_presidente = models.ImageField(upload_to="assinaturas/presidente/RequisicaoDesligamento", null=True, blank=True)

    # Assinatura do RH
    rh_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
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