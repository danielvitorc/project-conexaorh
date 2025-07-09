from conexaorh.models import RequisicaoPessoal
from conexaorh.utils.assinatura import assinar_formulario
from django import forms
from django.db import models
from django.forms import TimeInput, DateInput
from django.utils import timezone

AUTORIZACAO_CHOICES = [
        ('', 'Selecionar'),
        ('AUTORIZADO', 'Autorizar'),
        ('NÃO AUTORIZADO', 'Não autorizar'),
]

SIM_NAO_CHOICES = [('SIM', 'SIM'),('NÃO', 'NÃO'),]

# Formulário
class RequisicaoPessoalForm(forms.ModelForm):
    BENEFICIOS_CHOICES = [
        ('Plano Unimed CNU', 'Plano Unimed CNU'),
        ('Plano Saúde Hapvida', 'Plano Saúde Hapvida'),
        ('Alelo Mobilidade', 'Alelo Mobilidade'),
        ('Seguro de Vida', 'Seguro de Vida'),
    ]

    PROCESSOSELETIVO_CHOICES = [
        ('INTERNO', 'INTERNO'),
        ('MISTO', 'MISTO'),
        ('EXTERNO', 'EXTERNO'),
        ('SIGILOSO', 'SIGILOSO'),
    ]
    SEXO_CHOICES = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMININO', 'FEMININO'),
        ('INDIFERENTE', 'INDIFERENTE'),
    ]


    beneficios = forms.MultipleChoiceField(
        choices=BENEFICIOS_CHOICES,
        widget=forms.SelectMultiple(attrs={'size': 4}),  
        required=False,
        label='Benefícios'
    )   

    processo_seletivo = forms.MultipleChoiceField(
        choices=PROCESSOSELETIVO_CHOICES,
        widget= forms.SelectMultiple(attrs={'size': 4}),  
        required=False,
        label='Processo Seletivo'
    )

    sexo = forms.MultipleChoiceField(
        choices=SEXO_CHOICES,
        widget= forms.SelectMultiple(attrs={'size': 3}),
        required=False,
        label='Sexo'
    )
    exige_viagem = forms.MultipleChoiceField(
        choices=SIM_NAO_CHOICES,
        widget = forms.SelectMultiple(attrs={'size': 2}),
        required=False,
        label='Exige Viagem'
    )

    cnh = forms.MultipleChoiceField(
        choices=SIM_NAO_CHOICES,
        widget= forms.SelectMultiple(attrs={'size': 2}),
        required=False,
        label='CNH'
    )

    assinar_como_gestor = forms.BooleanField(
        required=False,
        label="Assinar como Gestor",
        help_text="Marque esta opção para assinar este formulário como gestor.",
    )
    class Meta:
        model = RequisicaoPessoal
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
            'n_rp',
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
            'horario_trabalho_inicio': TimeInput(attrs={'type': 'time'}),
            'horario_trabalho_fim': TimeInput(attrs={'type': 'time'}),
            'inicio_contrato': DateInput(attrs={'type': 'date'}),
            'termino_contrato': DateInput(attrs={'type': 'date'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.beneficios:
            self.initial['beneficios'] = self.instance.beneficios.split(',')

        if self.instance and self.instance.sexo:
            self.initial['sexo'] = self.instance.sexo.split(',')

        if self.instance and self.instance.processo_seletivo:
            self.initial['processo_seletivo'] = self.instance.processo_seletivo.split(',')

        if self.instance and self.instance.exige_viagem:
            self.initial['exige_viagem'] = self.instance.exige_viagem.split(',')

        if self.instance and self.instance.cnh:
            self.initial['cnh'] = self.instance.cnh.split(',')

    def clean_beneficios(self):
        return ','.join(self.cleaned_data['beneficios'])
    def clean_sexo(self):
        return ','.join(self.cleaned_data['sexo'])

    def clean_processo_seletivo(self):
        return ','.join(self.cleaned_data['processo_seletivo'])

    def clean_exige_viagem(self):
        return ','.join(self.cleaned_data['exige_viagem'])

    def clean_cnh(self):
        return ','.join(self.cleaned_data['cnh'])
    
    
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        # Converte todos os campos CharField e TextField para maiúsculas
        for field in instance._meta.get_fields():
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(instance, field.name)
                if value:
                    setattr(instance, field.name, value.upper())

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

# Aprovação e assinatura do Diretor
class DiretorFormRP(forms.ModelForm):
    assinar_como_diretor = forms.BooleanField(
        required=False,
        label="Assinar como Diretor",
        help_text="Marque esta opção para assinar este formulário como diretor.",
    )

    diretor_aprovacao = forms.ChoiceField(
        choices=AUTORIZACAO_CHOICES,
        label='Avaliação do Diretor',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = RequisicaoPessoal
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

# Aprovação e assinatura do Presidente    
class PresidenteFormRP(forms.ModelForm):

    assinar_como_presidente = forms.BooleanField(
        required=False,
        label="Assinar como Presidente",
        help_text="Marque esta opção para assinar este formulário como presidente.",
    )

    presidente_aprovacao = forms.ChoiceField(
        choices=AUTORIZACAO_CHOICES,
        label='Avaliação do Presidente',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = RequisicaoPessoal
        fields = ["assinatura_presidente", "presidente_aprovacao"]

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

# Aprovação e assinatura do RH    
class RHFormRP(forms.ModelForm):

    assinar_como_rh = forms.BooleanField(
        required=False,
        label="Assinar como RH/DP",
        help_text="Marque esta opção para assinar este formulário como RH/DP.",
    )

    rh_aprovacao = forms.ChoiceField(
        choices=AUTORIZACAO_CHOICES,
        label='Avaliação do RH/DP',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = RequisicaoPessoal
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