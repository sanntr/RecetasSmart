from .crear_usuarios import UsuarioForm
from django import forms

class FamiliaAdminForm(UsuarioForm):
    nombre_familia = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de la familia"})
    )