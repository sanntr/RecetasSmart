from django import forms
from .models import Receta, RecetaProducto
from django.forms import inlineformset_factory

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'pasos_receta']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la receta'}),
            'pasos_receta': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe los pasos...', 'rows': 4}),
        }

class RecetaProductoForm(forms.ModelForm):
    class Meta:
        model = RecetaProducto
        fields = ['producto', 'cantidad_uso']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_uso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad a usar'}),
        }

RecetaProductoFormSet = inlineformset_factory(
    Receta,
    RecetaProducto,
    form=RecetaProductoForm,
    extra=1,  # número de formularios vacíos por defecto
    can_delete=True
)