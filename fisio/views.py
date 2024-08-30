# views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Paciente, Profesional
from .forms import PacienteForm, ProfesionalForm


# Paciente Views
class PacienteListView(ListView):
    model = Paciente
    template_name = 'paciente_list.html'
    context_object_name = 'pacientes'

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'paciente_detail.html'
    context_object_name = 'paciente'

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente_form.html'
    success_url = reverse_lazy('paciente_list')

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente_form.html'
    success_url = reverse_lazy('paciente_list')

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente_list')

# Profesional Views
class ProfesionalListView(ListView):
    model = Profesional
    template_name = 'profesional_list.html'
    context_object_name = 'profesionales'

class ProfesionalDetailView(DetailView):
    model = Profesional
    template_name = 'profesional_detail.html'
    context_object_name = 'profesional'

class ProfesionalCreateView(CreateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = 'profesional_form.html'
    success_url = reverse_lazy('profesional_list')

class ProfesionalUpdateView(UpdateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = 'profesional_form.html'
    success_url = reverse_lazy('profesional_list')

class ProfesionalDeleteView(DeleteView):
    model = Profesional
    template_name = 'profesional_confirm_delete.html'
    success_url = reverse_lazy('profesional_list')
