from django import forms


class IniciarSesionForm(forms.Form):
    usuario = forms.CharField(
        max_length=150,
        required=True,
                widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
            'aria-describedby': 'user-addon'
        })
    )
    password = forms.CharField(
        required=True,
                widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'aria-describedby': 'pass-addon'
        })
    )

