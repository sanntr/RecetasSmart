from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'cantidad_disponible', 'unidad_medida']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad disponible'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),
        }

class AumentarStockForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, label="Cantidad a aumentar")