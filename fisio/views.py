# views.py
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Agendamiento, Paciente, Profesional, Servicio, Area
from .forms import AgendamientoForm, PacienteForm, ProfesionalForm, RegistroForm
from django.contrib.auth import login, authenticate
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import requires_csrf_token



#areas y servicios
class AreaListView(ListView):
    model = Area
    template_name = 'area_list.html'
    context_object_name = 'areas'

class AreaDetailView(DetailView):
    model = Area
    template_name = 'area_detail.html'
    context_object_name = 'area'

class AreaCreateView(CreateView):
    model = Area
    fields = '__all__'
    template_name = 'area_form.html'
    success_url = reverse_lazy('area_list')

class AreaUpdateView(UpdateView):
    model = Area
    fields = '__all__'
    template_name = 'area_form.html'
    success_url = reverse_lazy('area_list')

class AreaDeleteView(DeleteView):
    model = Area
    template_name = 'area_confirm_delete.html'
    success_url = reverse_lazy('area_list')

class ServicioListView(ListView):
    model = Servicio
    template_name = 'servicio_list.html'
    context_object_name = 'servicios'

class ServicioDetailView(DetailView):
    model = Servicio
    template_name = 'servicio_detail.html'
    context_object_name = 'servicio'

class ServicioCreateView(CreateView):
    model = Servicio
    fields = '__all__'
    template_name = 'servicio_form.html'
    success_url = reverse_lazy('servicio_list')

class ServicioUpdateView(UpdateView):
    model = Servicio
    fields = '__all__'
    template_name = 'servicio_form.html'
    success_url = reverse_lazy('servicio_list')

class ServicioDeleteView(DeleteView):
    model = Servicio
    template_name = 'servicio_confirm_delete.html'
    success_url = reverse_lazy('servicio_list')



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
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('login')  # Redirigir a la página de inicio de sesión después del registro
        else:
            messages.error(request, 'Por favor, corrija los errores.')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

@requires_csrf_token
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

class AgendamientoCreateView(CreateView):
    model = Agendamiento
    form_class = AgendamientoForm
    template_name = 'agendamiento_form.html'
    success_url = reverse_lazy('confirmacion_agendamiento')

    def form_valid(self, form):
        # Establecer el estado automáticamente a 'Pendiente de Confirmación'
        form.instance.estado = 'Pendiente de Confirmación'
        return super().form_valid(form)
    
class ConfirmacionAgendamientoView(TemplateView):
    template_name = 'confirmacion_agendamiento.html'

class AgendamientoListView(ListView):
    model = Agendamiento
    template_name = 'agendamiento_list.html'
    context_object_name = 'agendamientos'

# Vista para ver detalles de un agendamiento
class AgendamientoDetailView(DetailView):
    model = Agendamiento
    template_name = 'agendamiento_detail.html'
    context_object_name = 'agendamiento'