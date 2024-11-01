# views.py

import json
from django.utils import timezone  
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Agendamiento, Consulta, HorarioAtencion, Paciente, Profesional, Servicio, Area
from .forms import AgendamientoForm, PacienteForm, ProfesionalForm, RegistroForm
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import requires_csrf_token


#logoutViews
def logout_view(request):
    logout(request)
    return redirect('login')


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
        return render(request, 'calendario_admin.html')
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
        profesional = form.cleaned_data['profesional']
        servicio = form.cleaned_data['servicio']
        fecha = form.cleaned_data['fecha']
        hora = form.cleaned_data['hora']

        # Validar que la fecha no sea anterior a hoy
        if fecha < timezone.now().date():
            messages.error(self.request, "No se puede cargar un agendamiento en una fecha pasada.")
            return self.form_invalid(form)

        # Validar que el profesional tenga horario de atención
        horario_profesional = HorarioAtencion.objects.filter(
            profesional=profesional,
            servicio=servicio,
            fecha=fecha,
            hora_inicio__lte=hora,
            hora_fin__gte=hora
        ).exists()
        
        if not horario_profesional:
            messages.error(self.request, "El profesional no tiene horario de atención en esta especialidad y fecha.")
            return self.form_invalid(form)

        # Validar conflictos de agendamiento
        conflicto = Agendamiento.objects.filter(
            profesional=profesional,
            servicio=servicio,
            fecha=fecha,
            hora=hora
        ).exists()

        if conflicto:
            messages.error(self.request, "Ya existe un turno reservado para este profesional a esa hora.")
            return self.form_invalid(form)

        # Si no hay conflictos, guardar el agendamiento con estado 'Pendiente de Confirmación'
        form.instance.estado = 'Pendiente de Confirmación'
        messages.success(self.request, "Agendamiento creado exitosamente.")
        return super().form_valid(form)

class ConfirmacionAgendamientoView(TemplateView):
    template_name = 'agendamiento_confirmacion.html'

class AgendamientoListView(ListView):
    model = Agendamiento
    template_name = 'agendamiento_list.html'
    context_object_name = 'agendamientos'

class AgendamientoDetailView(DetailView):
    model = Agendamiento
    template_name = 'agendamiento_detail.html'
    context_object_name = 'agendamiento'

class AgendamientoUpdateView(UpdateView):
    model = Agendamiento
    form_class = AgendamientoForm
    template_name = 'agendamiento_form.html'
    success_url = reverse_lazy('agendamiento_list')

class AgendamientoDeleteView(DeleteView):
    model = Agendamiento
    template_name = 'agendamiento_confirm_delete.html'
    success_url = reverse_lazy('agendamiento_list')

class HorarioAtencionListView(ListView):
    model = HorarioAtencion
    template_name = 'horario_list.html'
    context_object_name = 'horarios_atencion'

    def get_queryset(self):
        return HorarioAtencion.objects.filter(profesional__isnull=False)

class HorarioAtencionDetailView(DetailView):
    model = HorarioAtencion
    template_name = 'horario_detail.html'
    context_object_name = 'horario_atencion'

class HorarioAtencionCreateView(CreateView):
    model = HorarioAtencion
    fields = '__all__'
    template_name = 'horario_atencion_form.html'
    success_url = reverse_lazy('horario_list')

class HorarioAtencionUpdateView(UpdateView):
    model = HorarioAtencion
    fields = '__all__'
    template_name = 'horario_atencion_form.html'
    success_url = reverse_lazy('horario_list')

class HorarioAtencionDeleteView(DeleteView):
    model = HorarioAtencion
    template_name = 'horario_confirm_delete.html'
    success_url = reverse_lazy('horario_list')




def calendario(request):
    # Obtenemos todos los agendamientos desde el modelo
    agendamientos = Agendamiento.objects.all()

    # Convertimos los agendamientos a una lista de diccionarios con el formato adecuado
    eventos = []
    for agendamiento in agendamientos:
        # Combinar fecha y hora en un objeto datetime
        start_datetime = datetime.combine(agendamiento.fecha, agendamiento.hora)

        # Calcular la hora de finalización (por ejemplo, 1 hora después del inicio)
        end_datetime = start_datetime + timedelta(hours=1)

        # Formateamos la información del evento para FullCalendar
        eventos.append({
            "title": f"{agendamiento.paciente.nombre} - {agendamiento.servicio.nombre}",
            "start": start_datetime.isoformat(),  # Formato ISO
            "end": end_datetime.isoformat(),      # Formato ISO
            "url": request.build_absolute_uri(f"/generar_consulta/{agendamiento.id}/"),
            "estado": agendamiento.estado,
            "backgroundColor": "#dc3545",
            "borderColor": "#dc3545"
        })
    # Pasamos los eventos serializados en JSON al template
    return render(request, 'calendario_admin.html', {
        'eventos_json': json.dumps(eventos)
    })
def generar_consulta(request, agendamiento_id):
    agendamiento = get_object_or_404(Agendamiento, id=agendamiento_id)
    if agendamiento.estado == 'en_curso':
        return redirect('calendario_admin')  # Redirigir al calendario si el agendamiento está en curso
    if request.method == 'POST':
        motivo_consulta = request.POST.get('motivo_consulta')
        diagnostico = request.POST.get('diagnostico')
        fecha_consulta = request.POST.get('fecha_consulta')
        Consulta.objects.create(
            paciente=agendamiento.paciente,
            profesional=agendamiento.profesional,
            fecha=fecha_consulta,
            servicio=agendamiento.servicio,
            hora=agendamiento.hora,
            motivo_consulta=motivo_consulta,
            diagnostico=diagnostico
        )
        agendamiento.estado = 'en_curso'
        agendamiento.save()
        return redirect('calendario_admin')
    return render(request, 'generar_consulta.html', {'agendamiento': agendamiento})
