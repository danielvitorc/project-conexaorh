from conexaorh.models import RequisicaoDesligamento
from conexaorh.utils.assinatura import assinar_formulario
from django import forms
from django.db import models
from django.forms import  DateInput
from django.utils import timezone

AUTORIZACAO_CHOICES = [
        ('', 'Selecionar'),
        ('AUTORIZADO', 'Autorizar'),
        ('NÃO AUTORIZADO', 'Não autorizar'),
]

SIM_NAO_CHOICES = [('SIM', 'SIM'),('NÃO', 'NÃO'),]

class RequisicaoDesligamentoForm(forms.ModelForm):

    TIPODESLIGAMENTO_CHOICES = [
        ('SEM JUSTA CAUSA', 'SEM JUSTA CAUSA'),
        ('POR JUSTA CAUSA', 'POR JUSTA CAUSA'),
        ('COMUM ACORDO', 'COMUM ACORDO'),
        ('TÉRMINO DE CONTRATO', 'TÉRMINO DE CONTRATO'),
        ('RESCISÃO ANTECIPADA CONTRATO DE EXPERIÊNCIA', 'RESCISÃO ANTECIPADA CONTRATO DE EXPERIÊNCIA'),
    ]
    MOTIVODESLIGAMENTO_CHOICES = [
        ('À PEDIDO DO COLABORADOR', 'À PEDIDO DO COLABORADOR'),
        ('REDUÇÃO DE QUADRO', 'REDUÇÃO DE QUADRO'),
        ('PROBLEMAS COM SUPERIORES', 'PROBLEMAS COM SUPERIORES'),
        ('INDISCIPLINA', 'INDISCIPLINA'),
        ('EXCESSO DE FALTAS', 'EXCESSO DE FALTAS'),
        ('INADEQUAÇÃO DO PROFISSIONAL À FUNÇÃO', 'INADEQUAÇÃO DO PROFISSIONAL À FUNÇÃO'),
        ('RELACIONAMENTO COM A EQUIPE INADEQUADO', 'RELACIONAMENTO COM A EQUIPE INADEQUADO'),
        ('BAIXO DESEMPENHO', 'BAIXO DESEMPENHO'),
        ('DESMOBILIZAÇÃO', 'DESMOBILIZAÇÃO'),
        ('REDUÇÃO DE CUSTO', 'REDUÇÃO DE CUSTO'),
    ]

    TIPOAVISO_CHOICES = [
        ('AVISO PRÉVIO TRABALHADO', 'AVISO PRÉVIO TRABALHADO'),
        ('AVISO PRÉVIO INDENIZADO', 'AVISO PRÉVIO INDENIZADO'),
    ]   

    tipo_desligamento = forms.MultipleChoiceField(
        choices= TIPODESLIGAMENTO_CHOICES,
        widget=forms.SelectMultiple(attrs={'size': 5}),
        required=False,
        label='Tipo de Desligamento'
    )

    motivo_desligamento = forms.MultipleChoiceField(
        choices= MOTIVODESLIGAMENTO_CHOICES,
        widget=forms.SelectMultiple(attrs={'size':10 }),
        required=False,
        label = 'Motivo do Desligamento'
    )
    tipo_aviso = forms.MultipleChoiceField(
        choices= TIPOAVISO_CHOICES,
        widget=forms.SelectMultiple(attrs={'size': 2}),
        required = False,
        label = 'Tipo de Aviso'
    )
    substituicao = forms.ChoiceField(
        choices =  SIM_NAO_CHOICES,
        widget=forms.RadioSelect(), 
        required = False,
        label = 'SERÁ NECESSÁRIO SUBSTITUIÇÃO?'
    )
    assinar_como_gestor = forms.BooleanField(
        required=False,
        label="Assinar como Gestor",
        help_text="Marque esta opção para assinar este formulário como gestor.",
    )

    class Meta:
        model = RequisicaoDesligamento
        exclude = [
            'data_solicitacao',
            'assinatura_diretor',
            'data_autorizacao_diretor',
            'assinatura_presidente',
            'data_autorizacao_presidente',
            'assinatura_rh',
            'data_autorizacao_rh',
            'dias_para_autorizacao_diretor',
            'dias_para_autorizacao_presidente',
            'dias_para_autorizacao_rh',
            'usuario',
            'assinatura_gestor',
            'imagem_assinatura_gestor',
            'imagem_assinatura_diretor',
            'imagem_assinatura_presidente',
            'imagem_assinatura_rh',
            'diretor_aprovacao',
            'presidente_aprovacao',
            'rh_aprovacao',
        ]
        widgets = {
            'data_desligamento': DateInput(attrs={'type': 'date'}),
            'data_admissao': DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'bloqueio_readmissao': 'Bloqueio de Readmissão'
        }


    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        # Converte todos os campos CharField e TextField para maiúsculas
        for field in instance._meta.get_fields():
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(instance, field.name)
                if value:
                    setattr(instance, field.name, value.upper())

        instance.tipo_desligamento = ", ".join(self.cleaned_data.get('tipo_desligamento', []))
        instance.motivo_desligamento = ", ".join(self.cleaned_data.get('motivo_desligamento', []))
        instance.tipo_aviso = ", ".join(self.cleaned_data.get('tipo_aviso', []))

        if user:
            instance.usuario = user
            if user.user_type == "gestor":
                assinar_formulario(instance, user, "assinatura_gestor", "data_autorizacao_gestor", "imagem_assinatura_gestor")
            elif user.user_type == "diretor":
                assinar_formulario(instance, user, "assinatura_diretor", "data_autorizacao_diretor", "imagem_assinatura_diretor")
            elif user.user_type == "presidente":
                assinar_formulario(instance, user, "assinatura_presidente", "data_autorizacao_presidente", "imagem_assinatura_presidente")
            elif user.user_type == "rh":
                assinar_formulario(instance, user, "assinatura_rh", "data_autorizacao_rh", "imagem_assinatura_rh")
        
        if commit:
            instance.save()
        return instance


class DiretorFormRD(forms.ModelForm):
    assinar_como_diretor = forms.BooleanField(
        required=False,
        label="Assinar como Diretor",
        help_text="Marque esta opção para assinar este formulário como gestor.",
    )

    diretor_aprovacao = forms.ChoiceField(
        choices=AUTORIZACAO_CHOICES,
        label='Avaliação do Diretor',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = RequisicaoDesligamento
        fields = ["assinatura_diretor", "diretor_aprovacao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        self.fields["assinatura_diretor"].widget = forms.HiddenInput()

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            assinar_formulario(
                instance, user,
                campo_assinatura="assinatura_diretor",
                campo_data="data_autorizacao_diretor",
                campo_imagem="imagem_assinatura_diretor",
                campo_dias="dias_para_autorizacao_diretor"
            )

        # Lógica para atribuir "NÃO APLICÁVEL" caso reprovado
        if instance.diretor_aprovacao == "NÃO AUTORIZADO":
            instance.presidente_aprovacao = "NÃO APLICÁVEL"
            instance.rh_aprovacao = "NÃO APLICÁVEL"

        if commit:
            instance.save()
        return instance

class PresidenteFormRD(forms.ModelForm):

    assinar_como_presidente = forms.BooleanField(
        required=False,
        label="Assinar como Presidente",
        help_text="Marque esta opção para assinar este formulário como Presidente.",
    )

    presidente_aprovacao = forms.ChoiceField(
        choices=AUTORIZACAO_CHOICES,
        label='Avaliação do Presidente',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = RequisicaoDesligamento
        fields = ["assinatura_presidente","presidente_aprovacao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        self.fields["assinatura_presidente"].widget = forms.HiddenInput()


    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            assinar_formulario(
                instance, user,
                campo_assinatura="assinatura_presidente",
                campo_data="data_autorizacao_presidente",
                campo_imagem="imagem_assinatura_presidente",
                campo_dias="dias_para_autorizacao_presidente"
            )

        # Lógica para atribuir "NÃO APLICÁVEL" caso reprovado
        if instance.presidente_aprovacao == "NÃO AUTORIZADO":
            instance.rh_aprovacao = "NÃO APLICÁVEL"

        if commit:
            instance.save()
        return instance

class RHFormRD(forms.ModelForm):

    assinar_como_rh = forms.BooleanField(
        required=False,
        label="Assinar como RH",
        help_text="Marque esta opção para assinar este formulário como RH/DP.",
    )

    rh_aprovacao = forms.ChoiceField(
        choices=AUTORIZACAO_CHOICES,
        label='Avaliação do RH/DP',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = RequisicaoDesligamento
        fields = ["assinatura_rh", "rh_aprovacao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        self.fields["assinatura_rh"].widget = forms.HiddenInput()

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            assinar_formulario(
                instance, user,
                campo_assinatura="assinatura_rh",
                campo_data="data_autorizacao_rh",
                campo_imagem="imagem_assinatura_rh",
                campo_dias="dias_para_autorizacao_rh"
            )

        if commit:
            instance.save()
        return instance