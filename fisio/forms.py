# forms.py
from django import forms
from .models import Paciente, Profesional
from django.contrib.auth.models import User
from .models import Perfil
from django.core.validators import validate_email


   # forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Perfil
from django.core.validators import validate_email

class RegistroForm(forms.ModelForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput())
    tipo = forms.ChoiceField(choices=Perfil.USER_TYPES)
    nro_documento = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo ya está registrado.')
        return email

    def save(self, commit=True):
        # Guardar usuario
        user = super(RegistroForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Guardar contraseña en formato hash
        if commit:
            user.save()

        # Guardar perfil
        perfil = Perfil(
            user=user,
            tipo=self.cleaned_data['tipo'],
            nro_documento=self.cleaned_data['nro_documento']
        )
        perfil.save()

        return user


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


