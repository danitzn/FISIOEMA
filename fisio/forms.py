# forms.py
from django import forms
from .models import Paciente, Profesional
from django.contrib.auth.models import User
from .models import Perfil

class RegistroForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    perfil = forms.ChoiceField(choices=Perfil.USER_TYPES)
    nro_documento = forms.CharField(max_length=20)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Perfil.objects.create(user=user, tipo=self.cleaned_data['perfil'], nro_documento=self.cleaned_data['nro_documento'])
        return user


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


