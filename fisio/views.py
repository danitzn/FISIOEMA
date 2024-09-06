# views.py
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Paciente, Profesional
from .forms import PacienteForm, ProfesionalForm, RegistroForm
from django.contrib.auth import login, authenticate
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required, user_passes_test

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


#perfiles de usuario def

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            error_message = 'Corrige los errores en el formulario.'
    else:
        form = RegistroForm()
        error_message = ''
    return render(request, 'registro.html', {'form': form, 'error_message': error_message})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            
            error_message = "Fallo autenticacion, favor contactar con administrador del sistema"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')



#decorador administrador
def es_administrador(user):
    return user.perfil.tipo == 'ADMINISTRADOR'

@login_required
@user_passes_test(es_administrador)
def vista_administrador(request):
    # Lógica para el administrador
    pass


#dashboard prueba
def es_administrador(user):
    return user.perfil.tipo == 'ADMINISTRADOR'

def es_profesional(user):
    return user.perfil.tipo == 'PROFESIONAL'

def es_paciente(user):
    return user.perfil.tipo == 'PACIENTE'

def es_administrativo(user):
    return user.perfil.tipo == 'ADMINISTRATIVO'

@login_required
def dashboard_view(request):
    perfil = request.user.perfil.tipo
    
    if perfil == 'ADMINISTRADOR':
        return render(request, 'dashboard_administrador.html')
    elif perfil == 'PROFESIONAL':
        return render(request, 'dashboard_profesional.html')
    elif perfil == 'PACIENTE':
        return render(request, 'dashboard_paciente.html')
    elif perfil == 'ADMINISTRATIVO':
        return render(request, 'dashboard_administrativo.html')
    else:
        return render(request, 'dashboard_generico.html')
    
    #home prueba
def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Cambia esto a la página del dashboard si es necesario
        else:
            error_message = "Fallo de autenticación, verifica tus datos."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')