from django import forms
from django.forms import TimeInput, DateInput
from .models import RequisicaoPessoal, MovimentacaoPessoal, RequisicaoDesligamento

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
    class Meta:
        model = RequisicaoPessoal
        exclude = [
            'data_solicitacao',
            'status_diretor',
            'data_autorizacao_diretor',
            'status_presidente',
            'data_autorizacao_presidente',
            'status_rh',
            'data_autorizacao_rh',
            'dias_para_autorizacao_diretor',
            'dias_para_autorizacao_presidente',
            'dias_para_autorizacao_rh',
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


class DiretorForm(forms.ModelForm):
    class Meta:
        model = RequisicaoPessoal
        fields = ["status_diretor"]  # Somente esse campo pode ser editado pelo diretor

class PresidenteForm(forms.ModelForm):
    class Meta:
        model = RequisicaoPessoal
        fields = ["status_presidente"]
        
class RHForm(forms.ModelForm):
    class Meta:
        model = RequisicaoPessoal
        fields = ["status_rh"]


class MovimentacaoPessoalForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoPessoal
        fields = ["nome_gestor", "cargo_gestor", "descricao"]


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
    substituicao = forms.MultipleChoiceField(
        choices = SIMNAO_CHOICES,
        widget= forms.SelectMultiple(attrs={'size': 2}),
        required = False,
        label = 'SERÁ NECESSÁRIO SUBSTITUIÇÃO?'
    )

    class Meta:
        model = RequisicaoDesligamento
        exclude = [
            'data_solicitacao',
            'status_diretor',
            'data_autorizacao_diretor',
            'status_presidente',
            'data_autorizacao_presidente',
            'status_rh',
            'data_autorizacao_rh',
            'dias_para_autorizacao_diretor',
            'dias_para_autorizacao_presidente',
            'dias_para_autorizacao_rh',
        ]
        

