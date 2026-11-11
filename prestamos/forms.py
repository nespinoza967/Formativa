import re

from django import forms

from .models import Categoria, Herramienta


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['codigo', 'nombre', 'categoria', 'estado', 'disponible', 'fecha_ingreso']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HER-000'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].strip().upper()
        if not re.fullmatch(r'HER-\d{3}', codigo):
            raise forms.ValidationError('El código debe tener el formato HER-000 (tres dígitos).')
        return codigo
