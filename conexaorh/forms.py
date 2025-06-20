from django import forms
from django.forms import TimeInput, DateInput
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from .models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento

User = get_user_model()

SIMNAO_CHOICES = [
        ('SIM', 'SIM'),
        ('NÃO', 'NÃO'),
]

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
        choices=SIMNAO_CHOICES,
        widget = forms.SelectMultiple(attrs={'size': 2}),
        required=False,
        label='Exige Viagem'
    )

    cnh = forms.MultipleChoiceField(
        choices=SIMNAO_CHOICES,
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
    
    @staticmethod
    def generate_signature_image(name: str) -> ContentFile:
        """Gera uma imagem com o nome do usuário como se fosse uma assinatura."""
        # Tamanho da imagem
        print("Gerando assinatura para:", name)

        # Fonte padrão (ou use uma .ttf customizada)
        try:
            font = ImageFont.truetype("BRADHITC.TTF", 40)
            print("Fonte carregada com sucesso.")
        except IOError:
            print("Fonte não encontrada, usando padrão.")
            font = ImageFont.load_default()
        
        # Calcular tamanho necessário do texto
        dummy_img = Image.new('RGBA', (1, 1))
        draw_dummy = ImageDraw.Draw(dummy_img)
        bbox = draw_dummy.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
 
        padding = 20
        img_width = text_width + padding * 2
        img_height = text_height + padding * 2

        img = Image.new('RGBA', (img_width, img_height), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        
        # Desenhar o texto centralizado verticalmente
        draw.text((padding, padding), name, font=font, fill=(0, 0, 0, 255))
        

        buffer = BytesIO()
        img.save(buffer, format='PNG')

        filename = f"assinatura_{name.lower().replace(' ', '_')}.png"
        return ContentFile(buffer.getvalue(), name=filename)
    
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
            nome_usuario = str(user.get_full_name() or user.username or "USUÁRIO")
            assinatura_img = self.generate_signature_image(nome_usuario)
        
        # Assinatura automática com base no tipo de usuário
        if user.user_type == "gestor":
            instance.assinatura_gestor = user
            instance.data_autorizacao_gestor = timezone.now()
            instance.imagem_assinatura_gestor.save(assinatura_img.name, assinatura_img, save=False)

        elif user.user_type == "diretor":
            instance.assinatura_diretor = user
            instance.data_autorizacao_diretor = timezone.now()
            instance.imagem_assinatura_diretor.save(assinatura_img.name, assinatura_img, save=False)

        elif user.user_type == "presidente":
            instance.assinatura_presidente = user
            instance.data_autorizacao_presidente = timezone.now()
            instance.imagem_assinatura_presidente.save(assinatura_img.name, assinatura_img, save=False)

        elif user.user_type == "rh":
            instance.assinatura_rh = user
            instance.data_autorizacao_rh = timezone.now()
            instance.imagem_assinatura_rh.save(assinatura_img.name, assinatura_img, save=False)

        if commit:
            instance.save()
        return instance


class DiretorForm(forms.ModelForm):

    assinar_como_diretor = forms.BooleanField(
        required=False,
        label="Assinar como Diretor",
        help_text="Marque esta opção para assinar este formulário como gestor.",
    )
    class Meta:
        model = RequisicaoPessoal
        fields = ["assinatura_diretor"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        self.fields["assinatura_diretor"].widget = forms.HiddenInput()

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            instance.assinatura_diretor = user
            instance.data_autorizacao_diretor = timezone.now()

            if instance.data_solicitacao:
                instance.dias_para_autorizacao_diretor = (
                    instance.data_autorizacao_diretor.date()
                    - instance.data_solicitacao.date()
                ).days

            # Gera imagem da assinatura se desejar
            assinatura_img = RequisicaoPessoalForm.generate_signature_image(
                str(user.get_full_name() or user.username or "USUÁRIO")
            )
            instance.imagem_assinatura_diretor.save(
                assinatura_img.name, assinatura_img, save=False
            )

        if commit:
            instance.save()
        return instance

class PresidenteForm(forms.ModelForm):

    assinar_como_presidente = forms.BooleanField(
        required=False,
        label="Assinar como Presidente",
        help_text="Marque esta opção para assinar este formulário como gestor.",
    )

    class Meta:
        model = RequisicaoPessoal
        fields = ["assinatura_presidente"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        self.fields["assinatura_presidente"].widget = forms.HiddenInput()


    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            instance.assinatura_presidente = user
            instance.data_autorizacao_presidente = timezone.now()

            if instance.data_solicitacao:
                instance.dias_para_autorizacao_presidente = (
                    instance.data_autorizacao_presidente.date()
                    - instance.data_solicitacao.date()
                ).days

            # Gera imagem da assinatura se desejar
            assinatura_img = RequisicaoPessoalForm.generate_signature_image(
                str(user.get_full_name() or user.username or "USUÁRIO")
            )
            instance.imagem_assinatura_presidente.save(
                assinatura_img.name, assinatura_img, save=False
            )

        if commit:
            instance.save()
        return instance
        
class RHForm(forms.ModelForm):

    assinar_como_rh = forms.BooleanField(
        required=False,
        label="Assinar como RH",
        help_text="Marque esta opção para assinar este formulário como gestor.",
    )

    class Meta:
        model = RequisicaoPessoal
        fields = ["assinatura_rh"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        self.fields["assinatura_rh"].widget = forms.HiddenInput()

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            instance.assinatura_rh = user
            instance.data_autorizacao_rh = timezone.now()

            if instance.data_solicitacao:
                instance.dias_para_autorizacao_rh = (
                    instance.data_autorizacao_rh.date()
                    - instance.data_solicitacao.date()
                ).days

            # Gera imagem da assinatura se desejar
            assinatura_img = RequisicaoPessoalForm.generate_signature_image(
                str(user.get_full_name() or user.username or "USUÁRIO")
            )
            instance.imagem_assinatura_rh.save(
                assinatura_img.name, assinatura_img, save=False
            )

        if commit:
            instance.save()
        return instance

class CompliceApprovalForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoPessoal
        fields = ['assinatura_complice']

class GestorPropostoApprovalForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoPessoal
        fields = ['assinatura_gestor_proposto']

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
        choices = SIMNAO_CHOICES,
        widget= forms.SelectMultiple(attrs={'size': 2}),
        required = False,
        label = 'SERÁ NECESSÁRIO SUBSTITUIÇÃO?'
    )

    class Meta:
        model = MovimentacaoPessoal
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
            'usuario'
            
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

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Lista de campos que NÃO devem ser convertidos para maiúsculas
        campos_excecao = ['gestor_proposto']

        # Converte todos os campos CharField e TextField para maiúsculas, exceto os de exceção
        for field in instance._meta.get_fields():
            if isinstance(field, (models.CharField, models.TextField)) and field.name not in campos_excecao:
                value = getattr(instance, field.name)
                if value:
                    setattr(instance, field.name, value.upper())

        instance.tipo_movimentacao = ", ".join(self.cleaned_data.get('tipo_movimentacao', []))
        instance.jutificativa_movimentacao = ", ".join(self.cleaned_data.get('jutificativa_movimentacao', []))
        instance.tipo_adicional = ", ".join(self.cleaned_data.get('tipo_adicional', []))
        instance.substituicao = ", ".join(self.cleaned_data.get('substituicao', []))
        
        if commit:
            instance.save()
        return instance


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
        choices =  SIMNAO_CHOICES,
        widget=forms.RadioSelect(), 
        required = False,
        label = 'SERÁ NECESSÁRIO SUBSTITUIÇÃO?'
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
        ]
        widgets = {
            'data_desligamento': DateInput(attrs={'type': 'date'}),
            'data_admissao': DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'bloqueio_readmissao': 'Bloqueio de Readmissão'
        }

    def save(self, commit=True):
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
        
        if commit:
            instance.save()
        return instance

