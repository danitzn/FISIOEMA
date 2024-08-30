# forms.py
from django import forms
from .models import Paciente, Profesional

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
        fields = '__all__'  # O especifica los campos que necesitas
