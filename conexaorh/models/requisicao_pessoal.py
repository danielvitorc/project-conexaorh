from django.conf import settings
from .users import CustomUser as User
from django.db import models
from django.utils import timezone
from conexaorh.models.organizacional import Filial, Base, Setor, Cargo 

class RequisicaoPessoal(models.Model):
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requisitante= models.CharField(max_length=100)
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, blank=True)
    base = models.ForeignKey(Base, on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
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
    
    sexo = models.CharField(max_length=100)
    exige_viagem = models.CharField(max_length=100)
    cnh = models.CharField(max_length=100)
    tipo_cnh = models.CharField(max_length=100)
    outros_cnh = models.CharField(max_length=100, null=True, blank=True)
    
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
    diretor_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
    assinatura_diretor = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_assinadas_como_diretor')
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/RequisicaoPessoal", null=True, blank=True)

    # Assinatura do presidente
    presidente_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
    assinatura_presidente = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='requisicoes_assinadas_como_presidente')
    data_autorizacao_presidente = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_presidente = models.ImageField(upload_to="assinaturas/presidente/RequisicaoPessoal", null=True, blank=True)

    # Assinatura do RH
    rh_aprovacao = models.CharField(default="PENDENTE", max_length=50, null=True, blank=True)
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