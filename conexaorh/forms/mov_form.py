from conexaorh.models import MovimentacaoPessoal
from conexaorh.models.users import CustomUser as User
from conexaorh.utils.assinatura import assinar_formulario
from django import forms
from django.core.files.base import ContentFile
from django.forms import TimeInput, DateInput
from django.db import models
from django.utils import timezone
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

SIM_NAO_CHOICES = [
        ('SIM', 'SIM'),
        ('NÃO', 'NÃO'),
]

AUTORIZACAO_CHOICES = [
        ('', 'Selecionar'),
        ('AUTORIZADO', 'Autorizar'),
        ('NÃO AUTORIZADO', 'Não autorizar'),
]


class MovimentacaoPessoalForm(forms.ModelForm):

    TIPOMOVIMENTACAO_CHOICES = [
        ('PROMOÇÃO HORIZONTAL', 'PROMOÇÃO HORIZONTAL'),
        ('TRANSFERÊNCIA DE ÁREA', 'TRANSFERÊNCIA DE ÁREA'),
        ('TRANSFERÊNCIA DE CONTRATO', 'TRANSFERÊNCIA DE CONTRATO'),
        ('PROMOÇÃO VERTICAL', 'PROMOÇÃO VERTICAL'),
        ('TRANSFERÊNCIA DE LOCALIDADE', 'TRANSFERÊNCIA DE LOCALIDADE'),
        ('ENQUADRAMENTO', 'ENQUADRAMENTO')
    ]

    TIPOADICIONAL_CHOICES = [
        ('PERICULOSIDADE', 'PERICULOSIDADE'),
        ('INSALUBRIDADE', 'INSALUBRIDADE'),
        ('AJUDA DE CUSTO', 'AJUDA DE CUSTO'),
        ('ADICIONAL', 'ADICIONAL')
    ]

    JUSTIFICATIVAMOVIMENTACAO_CHOICES = [
        ('REESTRUTURAÇÃO DO DEPARTAMENTO (EMPRESA/UNIDADE)', 'REESTRUTURAÇÃO DO DEPARTAMENTO (EMPRESA/UNIDADE)'),
        ('OPORTUNIDADE DE ASCENÇÃO', 'OPORTUNIDADE DE ASCENÇÃO'),
        ('INADEQUAÇÃO À ATIVIDADE DO DEPARTAMENTO', 'INADEQUAÇÃO À ATIVIDADE DO DEPARTAMENTO')
    ]

    tipo_movimentacao = forms.MultipleChoiceField(
        choices= TIPOMOVIMENTACAO_CHOICES,
        widget=forms.SelectMultiple(attrs={'size': 6}),
        required=False,
        label='Tipo de Movimentação'
    )
    
    tipo_adicional = forms.MultipleChoiceField(
        choices= TIPOADICIONAL_CHOICES,
        widget=forms.SelectMultiple(attrs={'size': 4}),
        required=False,
        label='Tipo de Adicional'
    )

    gestor_proposto = forms.ChoiceField(
        choices=[],                    
        label='Gestor Proposto',
        required=False,                
    )

    jutificativa_movimentacao = forms.MultipleChoiceField(
        choices= JUSTIFICATIVAMOVIMENTACAO_CHOICES,
        widget=forms.SelectMultiple(attrs={'size': 3}),
        required=False,
        label='Justificativa para Movimentação'
    )
    substituicao = forms.MultipleChoiceField(
        choices = SIM_NAO_CHOICES,
        widget= forms.SelectMultiple(attrs={'size': 2}),
        required = False,
        label = 'SERÁ NECESSÁRIO SUBSTITUIÇÃO?'
    )
    assinar_como_gestor_atual = forms.BooleanField(
        required=False,
        label="Assinar como Gestor Atual",
        help_text="Marque esta opção para assinar este formulário como gestor atual.",
    )

    class Meta:
        model = MovimentacaoPessoal
        labels  = {
            "outro_tipo": "Outro Tipo",
            "outro_info" : "Outras Informações "}
        exclude = [
            'data_solicitacao',
            'n_rp',
            'assinatura_diretor',
            'data_autorizacao_diretor',
            'assinatura_presidente',
            'data_autorizacao_presidente',
            'assinatura_rh',
            'assinatura_complice',
            'assinatura_gestor_proposto',
            'data_autorizacao_rh',
            'data_autorizacao_complice',
            'data_autorizacao_gestor_proposto',
            'dias_para_autorizacao_complice',
            'dias_para_autorizacao_gestor_proposto',
            'dias_para_autorizacao_diretor',
            'dias_para_autorizacao_presidente',
            'dias_para_autorizacao_rh',
            'usuario',
            'assinatura_gestor_atual',
            'imagem_assinatura_gestor_atual',
            'imagem_assinatura_complice',
            'imagem_assinatura_gestor_proposto',
            'imagem_assinatura_diretor',
            'imagem_assinatura_presidente',
            'imagem_assinatura_rh',
            'complice_aprovacao',
            'gestor_proposto_aprovacao',
            'diretor_aprovacao',
            'presidente_aprovacao',
            'rh_aprovacao'
        ]

        widgets = {
            'data_admissao': DateInput(attrs={'type': 'date'}),
            'data_movimentacao': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gestores = User.objects.filter(user_type='gestor')
        # monta lista de tuplas (valor, label)
        choices = [('', '— selecione —')] + [
            (g.username, g.get_full_name() or g.username) for g in gestores
        ]
        self.fields['gestor_proposto'].choices = choices
    
    def save(self, commit=True, user=None, gestor_role=None):
        instance = super().save(commit=False)

        # Lista de campos que NÃO devem ser convertidos para maiúsculas
        campos_excecao = ['gestor_proposto']

        # Converte todos os campos CharField e TextField para maiúsculas, exceto os de exceção
        for field in instance._meta.get_fields():
            if isinstance(field, (models.CharField, models.TextField)) and field.name not in campos_excecao:
                value = getattr(instance, field.name)
                if value:
                    setattr(instance, field.name, value.upper())

        if user:
            instance.usuario = user
            if user.user_type == "gestor":
                if gestor_role == "atual":
                    assinar_formulario(instance, user, "assinatura_gestor_atual", "data_autorizacao_gestor_atual", "imagem_assinatura_gestor_atual")
                elif gestor_role == "proposto":
                    assinar_formulario(instance, user, "assinatura_gestor_proposto", "data_autorizacao_gestor_proposto", "imagem_assinatura_gestor_proposto")
            elif user.user_type == "complice":
                assinar_formulario(instance, user, "assinatura_complice", "data_autorizacao_complice", "imagem_assinatura_complice")
            elif user.user_type == "diretor":
                assinar_formulario(instance, user, "assinatura_diretor", "data_autorizacao_diretor", "imagem_assinatura_diretor")
            elif user.user_type == "presidente":
                assinar_formulario(instance, user, "assinatura_presidente", "data_autorizacao_presidente", "imagem_assinatura_presidente")
            elif user.user_type == "rh":
                assinar_formulario(instance, user, "assinatura_rh", "data_autorizacao_rh", "imagem_assinatura_rh")


        instance.tipo_movimentacao = ", ".join(self.cleaned_data.get('tipo_movimentacao', []))
        instance.jutificativa_movimentacao = ", ".join(self.cleaned_data.get('jutificativa_movimentacao', []))
        instance.tipo_adicional = ", ".join(self.cleaned_data.get('tipo_adicional', []))
        instance.substituicao = ", ".join(self.cleaned_data.get('substituicao', []))

        
        if commit:
            instance.save()
        return instance

class CompliceFormMOV(forms.ModelForm):

    assinar_como_complice = forms.BooleanField(
        required=False,
        label="Assinar como Complice",
        help_text="Marque esta opção para assinar este formulário como Complice",
    )

    complice_aprovacao = forms.ChoiceField(
        choices=AUTORIZACAO_CHOICES,
        label='Avaliação do Complice',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = MovimentacaoPessoal
        fields = ['assinatura_complice', 'complice_aprovacao']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        self.fields["assinatura_complice"].widget = forms.HiddenInput()

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            assinar_formulario(
                instance, user,
                campo_assinatura="assinatura_complice",
                campo_data="data_autorizacao_complice",
                campo_imagem="imagem_assinatura_complice",
                campo_dias="dias_para_autorizacao_complice"
            )

        # Lógica para atribuir "NÃO APLICÁVEL" caso reprovado
        if instance.complice_aprovacao == "NÃO AUTORIZADO":
            instance.gestor_proposto_aprovacao == "NÃO APLICÁVEL"
            instance.diretor_aprovacao == "NÃO APLICÁVEL"
            instance.presidente_aprovacao = "NÃO APLICÁVEL"
            instance.rh_aprovacao = "NÃO APLICÁVEL"

        if commit:
            instance.save()
        return instance

class GestorPropostoMOV(forms.ModelForm):
    assinar_como_gestor_proposto = forms.BooleanField(
        required=False,
        label="Assinar como Gestor Proposto",
        help_text="Marque esta opção para assinar este formulário como Gestor Proposto",
    )

    gestor_proposto_aprovacao = forms.ChoiceField(
        choices=AUTORIZACAO_CHOICES,
        label='Avaliação do Gestor Proposto',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = MovimentacaoPessoal
        fields = ['assinatura_gestor_proposto', 'gestor_proposto_aprovacao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        self.fields["assinatura_gestor_proposto"].widget = forms.HiddenInput()

    def save(self, commit=True, user=None, gestor_role="proposto"):
        instance = super().save(commit=False)

        if user.user_type == "gestor" and gestor_role == "proposto":
            assinar_formulario(
                instance, user,
                campo_assinatura="assinatura_gestor_proposto",
                campo_data="data_autorizacao_gestor_proposto",
                campo_imagem="imagem_assinatura_gestor_proposto",
                campo_dias="dias_para_autorizacao_gestor_proposto"
            )

        # Lógica para atribuir "NÃO APLICÁVEL" caso reprovado
        if instance.gestor_proposto_aprovacao == "NÃO AUTORIZADO":
            instance.diretor_aprovacao == "NÃO APLICÁVEL"
            instance.presidente_aprovacao = "NÃO APLICÁVEL"
            instance.rh_aprovacao = "NÃO APLICÁVEL"

        if commit:
            instance.save()
        return instance

class DiretorFormMOV(forms.ModelForm):
    assinar_como_diretor = forms.BooleanField(
        required=False,
        label="Assinar como Diretor",
        help_text="Marque esta opção para assinar este formulário como Diretor.",
    )

    diretor_aprovacao = forms.ChoiceField(
        choices=AUTORIZACAO_CHOICES,
        label='Avaliação do Diretor',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = MovimentacaoPessoal
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

class PresidenteFormMOV(forms.ModelForm):

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
        model = MovimentacaoPessoal
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

class RHFormMOV(forms.ModelForm):

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
        model = MovimentacaoPessoal
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