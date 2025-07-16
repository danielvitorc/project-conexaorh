from django import forms
from conexaorh.models import Filial, Base, Setor, Curso, Cargo

class FilialForm(forms.ModelForm):
    class Meta:
        model = Filial
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BaseForm(forms.ModelForm):
    class Meta:
        model = Base
        fields = ['nome', 'filial']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'filial': forms.Select(attrs={'class': 'form-control'}),
        }

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome', 'base']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'base': forms.Select(attrs={'class': 'form-control'}),
        }

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nome', 'cursos', 'setores']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cursos': forms.SelectMultiple(attrs={'class': 'form-control select2-cursos'}),
            'setores': forms.SelectMultiple(attrs={'class': 'form-control select2-setores'}),
        }