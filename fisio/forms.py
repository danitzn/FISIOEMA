# forms.py
from django import forms
from .models import Paciente, Profesional
from django.contrib.auth.models import User
from .models import Perfil
from django.core.validators import validate_email

class RegistroForm(forms.ModelForm):
    email = forms.EmailField(required=True, validators=[validate_email])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo ya está registrado.')
        return email

class PacienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=['%d/%m/%Y']
    )
    
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg', 'placeholder': 'dd/mm/aaaa'}),
        }


class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = '__all__'


