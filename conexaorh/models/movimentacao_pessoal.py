from django.conf import settings
from .users import CustomUser as User
from django.db import models
from django.utils import timezone


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

    # Assinatura do Gestor Atual
    assinatura_gestor_atual = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='movimentacoes_assinadas_como_gestor_atual')
    data_autorizacao_gestor_atual = models.DateTimeField(null=True, blank=True, auto_now_add=True)    
    imagem_assinatura_gestor_atual = models.ImageField(upload_to="assinaturas/gestor/MovimentacaoPessoal", null=True, blank=True)

    # Assinatura do Complice
    complice_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
    assinatura_complice = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='movimentacoes_assinadas_como_complice')
    data_autorizacao_complice = models.DateTimeField(null=True, blank=True, auto_now_add=True)    
    imagem_assinatura_complice = models.ImageField(upload_to="assinaturas/complice/MovimentacaoPessoal", null=True, blank=True)

    # Assinatura do Gestor Proposto
    gestor_proposto_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
    assinatura_gestor_proposto = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='movimentacoes_assinadas_como_gestor_proposto')
    data_autorizacao_gestor_proposto = models.DateTimeField(null=True, blank=True, auto_now_add=True)    
    imagem_assinatura_gestor_proposto = models.ImageField(upload_to="assinaturas/gestor/MovimentacaoPessoal", null=True, blank=True)

    # Assinatura do Diretor
    diretor_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
    assinatura_diretor = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='movimentacoes_assinadas_como_diretor')
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/MovimentacaoPessoal", null=True, blank=True)

    # Assinatura do presidente
    presidente_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
    assinatura_presidente = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='movimentacoes_assinadas_como_presidente')
    data_autorizacao_presidente = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_presidente = models.ImageField(upload_to="assinaturas/presidente/MovimentacaoPessoal", null=True, blank=True)

    # Assinatura do RH
    rh_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
    assinatura_rh = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='movimentacoes_assinadas_como_rh')
    data_autorizacao_rh = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_rh = models.ImageField(upload_to="assinaturas/rh/MovimentacaoPessoal", null=True, blank=True)

    dias_para_autorizacao_complice = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_gestor_proposto = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_diretor = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_presidente = models.IntegerField(null=True, blank=True)
    dias_para_autorizacao_rh = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Movimentação: {self.colaborador_movimentado} ({self.tipo_movimentacao}) - {self.data_solicitacao.strftime('%d/%m/%Y')}"

    def assinar_gestor_atual(self, user):
        self.assinatura_gestor_atual = user
        self.data_assinatura_gestor_atual = timezone.now()
        self.save()

    def assinar_complice(self, user):
        self.assinatura_complice = user
        self.data_assinatura_complice = timezone.now()
        self.save()

    def assinar_gestor_proposto(self, user):
        self.assinatura_gestor_proposto = user
        self.data_assinatura_gestor_proposto = timezone.now()
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
