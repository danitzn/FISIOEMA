# views.py
import json, os, csv
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.db import connection, transaction
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from reportlab.lib.utils import ImageReader
from FISIOEMA import settings
from .models import Agendamiento, Consulta, FlujoCaja, HorarioAtencion, Informe, Paciente, Profesional, Responsable, Servicio, Area, SesionDetalle, Sesiones
from .forms import AgendamientoForm, HorarioForm, PacienteForm, ProfesionalForm, RegistroForm, ResponsableForm, SesionDetalleForm, SesionesForm, InformeForm
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import requires_csrf_token
from django.db.models import Sum
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.utils.timezone import now
from django.utils import timezone 
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas


#logoutViews
def logout_view(request):
    logout(request)
    return redirect('login')


#areas y servicios - Perfil Profesional
class AreaListProfView(ListView):
    model = Area
    template_name = 'area_list_prof.html'
    context_object_name = 'areasp'

class AreaDetailProfView(DetailView):
    model = Area
    template_name = 'area_detail_prof.html'
    context_object_name = 'areap'

#areas y servicios - Perfil Admin
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
    paginate_by = 10

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

# Servicio - Perfil Paciente
class ServicioListPacView(ListView):
    model = Servicio
    template_name = 'servicio_list_paciente.html'
    context_object_name = 'servicios'

class ServicioDetailPacView(DetailView):
    model = Servicio
    template_name = 'servicio_detail_paciente.html'
    context_object_name = 'servicio'

# Paciente - Perfil Admin Views
class PacienteListView(ListView):
    model = Paciente
    template_name = 'paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 10

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

# Paciente - Perfil Profesional Views
class PacienteListProfView(ListView):
    model = Paciente
    template_name = 'paciente_list_prof.html'
    context_object_name = 'pacientesp'
    paginate_by = 10

class PacienteDetailProfView(DetailView):
    model = Paciente
    template_name = 'paciente_detail_prof.html'
    context_object_name = 'pacientep'

class PacienteUpdateProfView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente_form_prof.html'
    success_url = reverse_lazy('paciente_list_prof')

#Paciente - Perfil Paciente Views
class PacienteDetailPacView(DetailView):
    model = Paciente
    template_name = 'paciente_detail_paciente.html'
    context_object_name = 'pacientespac'

# Profesional - PERFIL ADMIN Views
class ProfesionalListView(ListView):
    model = Profesional
    template_name = 'profesional_list.html'
    context_object_name = 'profesionales'
    paginate_by = 10

class ProfesionalDetailView(DetailView):
    model = Profesional
    template_name = 'profesional_detail.html'
    context_object_name = 'profesional'

class ProfesionalCreateView(CreateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = 'profesional_form.html'
    success_url = reverse_lazy('profesional_list')

    def form_invalid(self, form):
        # Captura el ValidationError y pásalo al formulario
        try:
            return super().form_invalid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.render_to_response(self.get_context_data(form=form))

class ProfesionalUpdateView(UpdateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = 'profesional_form.html'
    success_url = reverse_lazy('profesional_list')

class ProfesionalDeleteView(DeleteView):
    model = Profesional
    template_name = 'profesional_confirm_delete.html'
    success_url = reverse_lazy('profesional_list')

# Profesional - PERFIL PROFESIONAL Views
class ProfesionalListProfView(ListView):
    model = Profesional
    template_name = 'profesional_list_prof.html'
    context_object_name = 'profesionalesp'
    paginate_by = 10

class ProfesionalDetailProfView(DetailView):
    model = Profesional
    template_name = 'profesional_detail_prof.html'
    context_object_name = 'profesionalp'

# Profesional - PERFIL Paciente Views
class ProfesionalListPacView(ListView):
    model = Profesional
    template_name = 'profesional_list_paciente.html'
    context_object_name = 'profesionalespac'
    paginate_by = 10

class ProfesionalDetailPacView(DetailView):
    model = Profesional
    template_name = 'profesional_detail_paciente.html'
    context_object_name = 'profesionalpac'

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


class ResponsableCreateView(CreateView):
    model = Responsable
    form_class = ResponsableForm
    template_name = 'responsable_form.html'
    success_url = reverse_lazy('responsable_list')

class ResponsableUpdateView(UpdateView):
    model = Responsable
    form_class = ResponsableForm
    template_name = 'responsable_form.html'
    success_url = reverse_lazy('responsable_list')

class ResponsableDeleteView(DeleteView):
    model = Responsable
    template_name = 'responsable_confirm_delete.html'
    success_url = reverse_lazy('responsable_list')


class ResponsableDetailView(DetailView):
    model = Responsable
    template_name = 'responsable_detail.html'
    context_object_name = 'responsable'


class ResponsableListView(ListView):
    model = Responsable
    template_name = 'responsable_list.html'
    context_object_name = 'responsables'





# Agendamiento - Perfil Admin


class AgendamientoCreateView(CreateView):
    model = Agendamiento
    form_class = AgendamientoForm
    template_name = 'agendamiento_form.html'
    success_url = reverse_lazy('confirmacion_agendamiento')

    # def form_valid(self, form):
    #     profesional = form.cleaned_data['profesional']
    #     servicio = form.cleaned_data['servicio']
    #     fecha = form.cleaned_data['fecha']
    #     hora = form.cleaned_data['hora']
    #     tipo = form.cleaned_data['tipo']
    #     referencia_sesion = form.cleaned_data.get('referencia_sesion')

    #     # Validar tipo 'Sesión' con referencia_sesion
    #     if tipo == 'S':
    #         if not referencia_sesion:
    #             messages.error(self.request, "Debe seleccionar una sesión de referencia para el tipo 'Sesión'.")
    #             return self.form_invalid(form)

    #         sesion = Sesiones.validar_sesion(
    #             referencia_sesion=referencia_sesion,
    #             paciente=form.cleaned_data['paciente'],
    #             servicio=servicio
    #         )
    #         if not sesion:
    #             messages.error(self.request, "La sesión de referencia no es válida o ya finalizó.")
    #             return self.form_invalid(form)

    #         form.instance.referencia_sesion = referencia_sesion
    #     else:
    #         form.instance.referencia_sesion = None

    #     # Resto de la lógica
    #     form.instance.estado = 'pendiente'
    #     messages.success(self.request, "Agendamiento creado exitosamente.")
    #     return super().form_valid(form)

def form_valid(self, form):
    profesional = form.cleaned_data['profesional']
    servicio = form.cleaned_data['servicio']
    fecha = form.cleaned_data['fecha']
    hora = form.cleaned_data['hora']
    tipo = form.cleaned_data['tipo']
    paciente = form.cleaned_data['paciente']
    referencia_sesion = form.cleaned_data.get('referencia_sesion')

    # Validar el horario de atención
    horario_atencion = HorarioAtencion.objects.filter(
        profesional=profesional,
        servicio=servicio,
        fecha=fecha,
        hora_inicio__lte=hora,
        hora_fin__gt=hora
    ).first()

    if not horario_atencion:
        messages.error(self.request, "El horario no coincide con el horario de atención del profesional.")
        return self.form_invalid(form)

    # Validar tipo 'Sesión' con referencia_sesion
    if tipo == 'S':
        if not referencia_sesion:
            messages.error(self.request, "Debe seleccionar una sesión de referencia para el tipo 'Sesión'.")
            return self.form_invalid(form)

        sesion = Sesiones.validar_sesion(
            referencia_sesion=referencia_sesion,
            paciente=paciente,
            servicio=servicio
        )
        if not sesion:
            messages.error(self.request, "La sesión de referencia no es válida o ya finalizó.")
            return self.form_invalid(form)

        form.instance.referencia_sesion = referencia_sesion
    else:
        form.instance.referencia_sesion = None

    # Definir estado inicial como pendiente
    form.instance.estado = 'pendiente'

    messages.success(self.request, "Agendamiento creado exitosamente.")
    return super().form_valid(form)


class ConfirmacionAgendamientoView(TemplateView):
    template_name = 'agendamiento_confirmacion.html'

class AgendamientoListView(ListView):
    model = Agendamiento
    template_name = 'agendamiento_list.html'
    context_object_name = 'agendamientos'
    paginate_by = 10

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

# Agendamiento - Perfil Profesional

class AgendamientoCreateProfView(CreateView):
    model = Agendamiento
    form_class = AgendamientoForm
    template_name = 'agendamiento_form_prof.html'
    success_url = reverse_lazy('confirmacion_agendamiento_prof')

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

class ConfirmacionAgendamientoProfView(TemplateView):
    template_name = 'agendamiento_confirmacion_prof.html'

class AgendamientoListProfView(ListView):
    model = Agendamiento
    template_name = 'agendamiento_list_prof.html'
    context_object_name = 'agendamientosp'
    paginate_by = 10

class AgendamientoDetailProfView(DetailView):
    model = Agendamiento
    template_name = 'agendamiento_detail_prof.html'
    context_object_name = 'agendamientop'

class AgendamientoUpdateProfView(UpdateView):
    model = Agendamiento
    form_class = AgendamientoForm
    template_name = 'agendamiento_form_prof.html'
    success_url = reverse_lazy('agendamiento_list_prof')

class AgendamientoDeleteProfView(DeleteView):
    model = Agendamiento
    template_name = 'agendamiento_confirm_delete_prof.html'
    success_url = reverse_lazy('agendamiento_list_prof')

#Horario Atencion - Perfil Profesional
class HorarioAtencionListProfView(ListView):
    model = HorarioAtencion
    template_name = 'horario_list_prof.html'
    context_object_name = 'horarios_atencionp'
    paginate_by = 10

    def get_queryset(self):
        return HorarioAtencion.objects.filter(profesional__isnull=False)

class HorarioAtencionDetailProfView(DetailView):
    model = HorarioAtencion
    template_name = 'horario_detail_prof.html'
    context_object_name = 'horario_atencionp'

#Horario Atencion - Perfil Paciente
class HorarioAtencionListPacView(ListView):
    model = HorarioAtencion
    template_name = 'horario_list_paciente.html'
    context_object_name = 'horarios_atencion'
    paginate_by = 10

    def get_queryset(self):
        return HorarioAtencion.objects.filter(profesional__isnull=False)

class HorarioAtencionDetailPacView(DetailView):
    model = HorarioAtencion
    template_name = 'horario_detail_paciente.html'
    context_object_name = 'horario_atencion'

# Horario de Atencion - Perfil Admin 
class HorarioAtencionListView(ListView):
    model = HorarioAtencion
    template_name = 'horario_list.html'
    context_object_name = 'horarios_atencionp'
    paginate_by = 10

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

    def form_invalid(self, form):
        # Captura el ValidationError y pásalo al formulario
        try:
            return super().form_invalid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.render_to_response(self.get_context_data(form=form))

class HorarioAtencionUpdateView(UpdateView):
    model = HorarioAtencion
    fields = '__all__'
    form_class = HorarioForm
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
        end_datetime = start_datetime + timedelta(hours=1)  # Duración estimada

        # Definir colores según el tipo de agendamiento
        if agendamiento.tipo == 'E':  # Evaluación
            background_color = '#FF0000'  # Rojo
            border_color = '#FF0000'
        elif agendamiento.tipo == 'S':  # Sesión
            if agendamiento.estado == 'pendiente':  # Estado pendiente para sesiones
                background_color = '#D4A017'  # Mostaza
                border_color = '#D4A017'
            else:  # Estado en_curso o finalizado para sesiones
                background_color = '#28a745' if agendamiento.estado == 'en_curso' else '#17a2b8'
                border_color = background_color
        elif agendamiento.tipo == 'I':  # Informe
            background_color = '#000000'  # Negro
            border_color = '#000000'
        else:
            background_color = '#dc3545'  # Default rojo
            border_color = '#dc3545'

        # Formateamos la información del evento para FullCalendar
        eventos.append({
            "title": f"{agendamiento.paciente.nombre} - {agendamiento.servicio.nombre}",
            "start": start_datetime.isoformat(),  # Formato ISO
            "end": end_datetime.isoformat(),      # Formato ISO
            "url": request.build_absolute_uri(f"/generar_consulta/{agendamiento.id}/"),
            "estado": agendamiento.estado,
            "tipo": agendamiento.tipo,  # Añade el tipo para uso en el frontend
            "backgroundColor": background_color,
            "borderColor": border_color
        })

    # Pasamos los eventos serializados en JSON al template
    eventos_json = json.dumps(eventos) if eventos else '[]'
    return render(request, 'dashboard_administrador.html', {
        'eventos_json': eventos_json
    })


class FlujoCajaListView(ListView):
    model = FlujoCaja
    template_name = 'flujo_caja_list.html'
    context_object_name = 'flujo_dinero'
    paginate_by = 10

    def get_queryset(self):
        queryset = FlujoCaja.objects.all()
        today = timezone.now().date()

        # Obtén los filtros de las fechas
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')

        if fecha_desde and fecha_hasta:
            queryset = queryset.filter(fecha__range=[fecha_desde, fecha_hasta])
        else:
            # Filtrar solo los registros de hoy si no se proporcionan fechas
            queryset = queryset.filter(fecha=today)

        # Calcular totales para entradas y salidas
        self.total_entradas = queryset.filter(tipo_operacion='R').aggregate(total=Sum('monto'))['total'] or 0
        self.total_salidas = queryset.filter(tipo_operacion='P').aggregate(total=Sum('monto'))['total'] or 0

        return queryset

    def get_context_data(self, **kwargs):
        # Añadir el total de entradas y salidas al contexto
        context = super().get_context_data(**kwargs)
        context['total_entradas'] = self.total_entradas
        context['total_salidas'] = self.total_salidas
        return context
def generar_consulta(request, agendamiento_id):
    agendamiento = get_object_or_404(Agendamiento, id=agendamiento_id)

    # Si el tipo es Sesión, obtener la sesión asociada desde referencia_sesion
    sesion = None
    if agendamiento.referencia_sesion:
        sesion = get_object_or_404(Sesiones, id=agendamiento.referencia_sesion)

    # Verificar si el agendamiento está en curso
    if agendamiento.estado == 'en_curso':
        return redirect('calendario_admin')  # Redirigir al calendario si el agendamiento está en curso

    if agendamiento.tipo == 'E':  # Evaluación
        if request.method == 'POST':
            motivo_consulta = request.POST.get('motivo_consulta')
            diagnostico = request.POST.get('diagnostico')
            fecha_consulta = request.POST.get('fecha_consulta', date.today())

            # Crear la consulta
            nueva_consulta = Consulta.objects.create(
                paciente=agendamiento.paciente,
                profesional=agendamiento.profesional,
                fecha=fecha_consulta,
                servicio=agendamiento.servicio,
                hora=agendamiento.hora,
                motivo_consulta=motivo_consulta,
                diagnostico=diagnostico
            )

            # Actualizar estado del agendamiento
            agendamiento.estado = 'finalizado'
            agendamiento.save()

            return redirect('calendario_admin')

        # Redirigir al formulario de sesiones
        sesiones_form = SesionesForm()
        return render(request, 'generar_consulta.html', {'sesionesForm': sesiones_form, 'agendamiento': agendamiento})

    elif agendamiento.tipo == 'S':  # Sesión
        sesiones_form = SesionDetalleForm(request.POST or None)

        if request.method == 'POST' and sesiones_form.is_valid():
            nueva_sesion = sesiones_form.save(commit=False)
            nueva_sesion.sesion = sesion  # Asigna la sesión obtenida desde referencia_sesion
            nueva_sesion.paciente = agendamiento.paciente
            nueva_sesion.agendamiento = agendamiento
            nueva_sesion.servicio = agendamiento.servicio
            nueva_sesion.save()

            # Incrementar sesiones realizadas
            sesion.cantidad_realizadas += 1
            sesion.save()

            # Actualizar estado del agendamiento
            agendamiento.estado = 'finalizado'
            agendamiento.save()

            return redirect('calendario_admin')

        return render(request, 'sesion_detalle.html', {
            'agendamiento': agendamiento,
            'sesionesDetalle_form': sesiones_form
        })

    elif agendamiento.tipo == 'I':  # Informe
        informe = None
        form = InformeForm(request.POST or None, initial={
            'paciente': agendamiento.paciente,
            'profesional': agendamiento.profesional,
            'fecha': date.today()
        })

        if request.method == 'POST' and form.is_valid():
            informe = form.save(commit=False)
            informe.paciente = agendamiento.paciente
            informe.profesional = agendamiento.profesional
            informe.fecha = date.today()
            informe.save()

            # Actualizar estado del agendamiento
            agendamiento.estado = 'finalizado'
            agendamiento.save()

            return redirect('calendario_admin')

        return render(request, 'informe_form.html', {
            'form': form,
            'agendamiento': agendamiento,
            'informe': informe
        })
    
    
def buscar_consultas_por_ci(request):
    consultas = None
    nrodocumento = None

    if request.method == "POST":
        nrodocumento = request.POST.get("nrodocumento")
        consultas = Consulta.objects.filter(paciente__nrodocumento=nrodocumento, estado__in=['Pendiente', 'Pago Parcial', 'P', 'PP'])

    return render(request, "buscar_consultas.html", {"consultas": consultas, "nrodocumento": nrodocumento})

def cobrar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    if request.method == "POST":
        medio_pago = request.POST.get("medio_pago")
        monto = consulta.servicio.monto

        # Crear registro en FlujoCaja sin el campo consulta
        FlujoCaja.objects.create(
            persona=consulta.paciente.nrodocumento,  # Usamos el CI del paciente como persona
            fecha=consulta.fecha,                    # Usar la fecha de la consulta
            monto=monto,
            tipo_operacion="R",                      # 'R' para recibo (entrada de dinero)
            medio_pago=medio_pago,
        )

        # Cambiar estado de la consulta a 'C' de Cancelado
        consulta.estado = "C"
        consulta.save()
    
        return redirect("buscar_consultas_por_ci")  # Redirige de vuelta a la página de búsqueda

    return render(request, "cobrar_consulta.html", {"consulta": consulta})



#reportes
def reporte_consultas(request):
    # Obtener parámetros del filtro de fecha
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Filtrar consultas por rango de fecha si se proporcionan fechas
    consultas = Consulta.objects.all()
    if start_date and end_date:
        consultas = consultas.filter(fecha__range=[start_date, end_date])
    
    # Renderizar la página HTML
    if 'export_pdf' in request.GET:
        return exportar_pdf(consultas)

    if 'export_excel' in request.GET:
        return exportar_excel(consultas)

    return render(request, 'resumen.html', {
        'consultas': consultas,
        'start_date': start_date,
        'end_date': end_date
    })



def exportar_pdf(consultas):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_consultas.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Ruta a la imagen de cabecera
    imagen_path = f"{settings.BASE_DIR}/static/images/fisio1.jpg"  
    pie_imagen_path = f"{settings.BASE_DIR}/static/images/fisio6.jpg"  

    # Dibujar cabecera con imagen
    if os.path.exists(imagen_path):  # Verifica si la imagen existe
        c.drawImage(ImageReader(imagen_path), 50, height - 100, width=500, height=70)

    # Título principal
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 120, "Reporte de Consultas")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 140, "Generado automáticamente por el sistema")

    # Títulos de columnas
    y = height - 180
    c.drawString(50, y, "Nombre de Paciente")
    c.drawString(250, y, "Motivo de la Consulta")
    c.drawString(450, y, "Diagnóstico")
    c.line(50, y - 5, width - 50, y - 5)  # Línea divisoria
    y -= 30

    # Agregar contenido de las consultas
    for consulta in consultas:
        if y < 80:  # Si queda poco espacio, añade una nueva página
            # Dibujar pie de página antes de cambiar de página
            if os.path.exists(pie_imagen_path):
                c.drawImage(ImageReader(pie_imagen_path), 50, 30, width=500, height=50)
            c.showPage()
            y = height - 100
        c.drawString(50, y, f"{consulta.paciente.nombre} {consulta.paciente.apellido}")
        c.drawString(250, y, consulta.motivo_consulta[:50])  # Limitar texto
        c.drawString(450, y, consulta.diagnostico[:50])  # Limitar texto
        y -= 20

    # Dibujar el pie de página en la última página
    if os.path.exists(pie_imagen_path):
        c.drawImage(ImageReader(pie_imagen_path), 50, 30, width=500, height=50)
    else:
        c.setFont("Helvetica", 10)
        c.drawString(50, 30, "Reporte generado por el sistema - FISIOEMA")

    c.showPage()
    c.save()
    return response


# Función para generar Excel
def exportar_excel(consultas):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_consultas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre de Paciente', 'Motivo de la Consulta', 'Diagnóstico'])

    for consulta in consultas:
        writer.writerow([
            f"{consulta.paciente.nombre} {consulta.paciente.apellido}",
            consulta.motivo_consulta,
            consulta.diagnostico
        ])

    return response

def generar_informe_pdf(request, pk):
    informe = get_object_or_404(Informe, pk=pk)

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_{pk}.pdf"'

    # Configurar el canvas y el diseño
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, f"Informe de {informe.paciente}")

    # Línea divisoria
    p.setStrokeColor(colors.grey)
    p.line(50, height - 60, width - 50, height - 60)

    # Detalles del informe
    p.setFont("Helvetica", 12)
    y = height - 100  # Posición inicial en Y
    p.drawString(50, y, f"Profesional: {informe.profesional}")
    y -= 20
    p.drawString(50, y, f"Fecha del Informe: {informe.fecha_informe}")
    y -= 20
    p.drawString(50, y, "Descripción:")
    y -= 20
    p.drawString(70, y, informe.descripcion)

    # Finalizar página
    p.showPage()
    p.save()

    return response


class ReporteAgendamientosView(TemplateView):
    template_name = 'reporte_agendamientos.html'

    def get(self, request, *args, **kwargs):
        # Obtener filtros desde el request
        tipo = request.GET.get('tipo', 'todos')  # Valores: 'E', 'S', 'I', o 'todos'
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')

        # Filtrar agendamientos por fechas y tipo
        agendamientos = Agendamiento.objects.all()

        if fecha_desde:
            agendamientos = agendamientos.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            agendamientos = agendamientos.filter(fecha__lte=fecha_hasta)
        if tipo != 'todos':
            agendamientos = agendamientos.filter(tipo=tipo)

        # Agrupar y contar agendamientos por servicio
        tipos = {'E': 'Evaluaciones', 'S': 'Sesiones', 'I': 'Informes'}
        resumen = {
            nombre: agendamientos.filter(tipo=tipo).values('servicio__nombre').annotate(total=Count('id'))
            for tipo, nombre in tipos.items()
        }

        # Pasar los datos al template
        context = {
            'resumen': resumen,
            'filtros': {
                'tipo': tipo,
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta,
            },
        }
        return render(request, self.template_name, context)


#generar sesiones
def obtener_sesiones(request):
    paciente_id = request.GET.get('paciente')
    servicio_id = request.GET.get('servicio')

    if paciente_id and servicio_id:
        sesiones = Sesiones.objects.filter(
            paciente_id=paciente_id, 
            servicio_id=servicio_id,
            finalizado=False  # Filtrar sesiones no finalizadas
        )
        sesiones_data = [{'id': sesion.id, 'nombre': str(sesion)} for sesion in sesiones]
        return JsonResponse(sesiones_data, safe=False)
    return JsonResponse([], safe=False)


class DetalleSesionesView(TemplateView):
    template_name = 'sesionesform.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Sesionesform'] = SesionesForm()  # Incluye el formulario
        return context

def sesiones_view(request):
    if request.method == "POST":
        form = SesionesForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirecciona o muestra un mensaje de éxito
            return redirect('nombre_de_la_url')  # Reemplaza con tu URL de redirección
    else:
        form = SesionesForm()
    
    return render(request, 'tu_template.html', {'Sesionesform': form})


# -------------------- Cobranzas View --------------------


class CobranzasView(View):
    template_name = "cobranzas.html"

    def get(self, request):
        paciente_id = request.GET.get("paciente")
        fecha_desde = request.GET.get("fecha_desde")
        fecha_hasta = request.GET.get("fecha_hasta")
        servicio_id = request.GET.get("servicio")

        # Parámetros para la consulta
        params = []
        filtros = ""

        if paciente_id:
            filtros += " AND p.id = %s"
            params.append(paciente_id)

        if fecha_desde and fecha_hasta:
            filtros += " AND {table}.fecha BETWEEN %s AND %s"
            params.extend([fecha_desde, fecha_hasta])

        if servicio_id:
            filtros += " AND ser.id = %s"
            params.append(servicio_id)

        sql = f"""
        SELECT 
            c.fecha AS fecha,
            c.diagnostico AS descripcion,
            ser.nombre AS servicio,
            p.nombre || ' ' || p.apellido AS paciente,
            ser.monto AS monto,
            'Consulta' as tipo
        FROM 
            fisio_consulta c
        INNER JOIN 
            fisio_servicio ser ON ser.id = c.servicio_id
        INNER JOIN 
            fisio_paciente p ON p.id = c.paciente_id
        WHERE 
            c.estado_prof IN ('P', 'Pendiente')
            {filtros.format(table='c')}
        
        UNION ALL
        
        SELECT 
            i.fecha_informe AS fecha,
            i.descripcion AS descripcion,
            ser.nombre AS servicio,
            p.nombre || ' ' || p.apellido AS paciente,
            ser.monto AS monto,
            'Informe' as tipo
        FROM 
            fisio_informe i
        INNER JOIN 
            fisio_servicio ser ON ser.id = i.servicio_id
        INNER JOIN 
            fisio_paciente p ON p.id = i.paciente_id
        WHERE 
            i.estado_prof IN ('P', 'Pendiente')
            {filtros.replace('fecha', 'fecha_informe').format(table='i')}
        
        UNION ALL
        
        SELECT 
            sd.fecha AS fecha,
            sd.observaciones AS descripcion,
            ser.nombre AS servicio,
            p.nombre || ' ' || p.apellido AS paciente,
            ser.monto AS monto,
            'Sesión' as tipo
        FROM 
            fisio_sesiondetalle sd
        INNER JOIN 
            fisio_sesiones s ON s.id = sd.sesion_id
        INNER JOIN 
            fisio_consulta c ON c.id = s.consulta_id
        INNER JOIN 
            fisio_servicio ser ON ser.id = s.servicio_id
        INNER JOIN 
            fisio_paciente p ON p.id = s.paciente_id
        WHERE 
            sd.estado_prof IN ('P', 'Pendiente')
            {filtros.format(table='sd')}
        ORDER BY fecha DESC
        """

        # Ejecutar la consulta SQL
        with connection.cursor() as cursor:
            cursor.execute(sql, params * 3)  # Multiplicamos los parámetros por 3 debido al UNION ALL
            resultados = cursor.fetchall()

        # Convertir los resultados a un diccionario
        cobros = [
            {
                'id': idx,
                'fecha': row[0],
                'descripcion': row[1],
                'servicio': row[2],
                'paciente': row[3],
                'monto': row[4],
                'tipo': row[5]
            }
            for idx, row in enumerate(resultados, start=1)
        ]

        pacientes = Paciente.objects.all()
        servicios = Servicio.objects.all()
        medios_pago = ["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia Bancaria"]

        context = {
            "cobros": cobros, 
            "pacientes": pacientes, 
            "servicios": servicios,
            "medios_pago": medios_pago,
            "filtros": {
                "paciente_id": paciente_id,
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta,
                "servicio_id": servicio_id
            }
        }

        return render(request, self.template_name, context)

    def post(self, request):
        seleccionados = request.POST.getlist('seleccionados')
        medio_pago = request.POST.get('medio_pago')

        if seleccionados and medio_pago:
            with transaction.atomic():
                # Convertir IDs a enteros
                seleccionados = [int(id) for id in seleccionados]

                # Crear la lista de placeholders para el IN
                placeholders = ','.join(['?' for _ in seleccionados])

                # Ejecutar la consulta SQL para obtener los cobros seleccionados
                sql = f"""
                SELECT 
                    c.id as id,
                    c.fecha as fecha,
                    c.diagnostico as descripcion,
                    ser.nombre as servicio,
                    p.nombre || ' ' || p.apellido as paciente,
                    ser.monto as monto,
                    'Consulta' as tipo
                FROM fisio_consulta c
                INNER JOIN fisio_servicio ser ON ser.id = c.servicio_id
                INNER JOIN fisio_paciente p ON p.id = c.paciente_id
                WHERE c.id IN ({placeholders})

                UNION ALL

                SELECT 
                    i.id as id,
                    i.fecha_informe as fecha,
                    i.descripcion as descripcion,
                    ser.nombre as servicio,
                    p.nombre || ' ' || p.apellido as paciente,
                    ser.monto as monto,
                    'Informe' as tipo
                FROM fisio_informe i
                INNER JOIN fisio_servicio ser ON ser.id = i.servicio_id
                INNER JOIN fisio_paciente p ON p.id = i.paciente_id
                WHERE i.id IN ({placeholders})

                UNION ALL

                SELECT 
                    sd.id as id,
                    sd.fecha as fecha,
                    sd.observaciones as descripcion,
                    ser.nombre as servicio,
                    p.nombre || ' ' || p.apellido as paciente,
                    ser.monto as monto,
                    'Sesión' as tipo
                FROM fisio_sesiondetalle sd
                INNER JOIN fisio_sesiones s ON s.id = sd.sesion_id
                INNER JOIN fisio_servicio ser ON ser.id = s.servicio_id
                INNER JOIN fisio_paciente p ON p.id = s.paciente_id
                WHERE sd.id IN ({placeholders})
                """

                with connection.cursor() as cursor:
                    # Multiplicamos seleccionados por 3 debido a los tres IN en la consulta
                    cursor.execute(sql, seleccionados * 3)
                    resultados = cursor.fetchall()

                cobros_seleccionados = [
                    {
                        'id': row[0],
                        'fecha': row[1],
                        'descripcion': row[2],
                        'servicio': row[3],
                        'paciente': row[4],
                        'monto': row[5],
                        'tipo': row[6]
                    }
                    for row in resultados
                ]

                # Calcular el monto total
                monto_total = sum(cobro['monto'] for cobro in cobros_seleccionados)

                # Registrar operación en flujo de caja
                FlujoCaja.objects.create(
                    persona=cobros_seleccionados[0]['paciente'],
                    monto=monto_total,
                    tipo_operacion='Recibo (Entrada)',
                    medio_pago=medio_pago,
                    fecha=cobros_seleccionados[0]['fecha'],
                    descripcion=f"Cobro al paciente {cobros_seleccionados[0]['paciente']} por servicios"
                )

                # Actualizar el estado a 'Cancelado'
                SesionDetalle.objects.filter(id__in=seleccionados).update(estado_pago='C')
                Consulta.objects.filter(id__in=seleccionados).update(estado_pago='C')
                Informe.objects.filter(id__in=seleccionados).update(estado_pago='C')

                # Generar PDF
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="cobros_paciente.pdf"'
                p = canvas.Canvas(response)
                p.drawString(100, 800, "Cobros al Paciente")
                y = 750
                for cobro in cobros_seleccionados:
                    p.drawString(100, y, f"Fecha: {cobro['fecha']}, Descripción: {cobro['descripcion']}, Servicio: {cobro['servicio']}, Monto: {cobro['monto']}")
                    y -= 20
                p.showPage()
                p.save()

                return response

        return redirect('cobranzas')


# -------------------- Pagos View --------------------

class PagosView(View):
    template_name = "pagos.html"

    def get(self, request):
        profesional_id = request.GET.get("profesional")
        fecha_desde = request.GET.get("fecha_desde")
        fecha_hasta = request.GET.get("fecha_hasta")
        servicio_id = request.GET.get("servicio")

        # Parámetros para la consulta
        params = []
        filtros = ""

        if profesional_id:
            filtros += " AND p.id = %s"
            params.append(profesional_id)

        if fecha_desde and fecha_hasta:
            filtros += " AND {table}.fecha BETWEEN %s AND %s"
            params.extend([fecha_desde, fecha_hasta])

        if servicio_id:
            filtros += " AND ser.id = %s"
            params.append(servicio_id)

        sql = f"""
        SELECT 
            c.fecha AS fecha,
            c.diagnostico AS descripcion,
            ser.nombre AS servicio,
            p.nombre || ' ' || p.apellido AS profesional,
            ser.monto * 0.7 AS monto,
            'Consulta' as tipo
        FROM 
            fisio_consulta c
        INNER JOIN 
            fisio_servicio ser ON ser.id = c.servicio_id
        INNER JOIN 
            fisio_profesional p ON p.id = c.profesional_id
        WHERE 
            c.estado_prof IN ('P', 'Pendiente')
            {filtros.format(table='c')}
        
        UNION ALL
        
        SELECT 
            i.fecha_informe AS fecha,
            i.descripcion AS descripcion,
            ser.nombre AS servicio,
            p.nombre || ' ' || p.apellido AS profesional,
            ser.monto * 0.7 AS monto,
            'Informe' as tipo
        FROM 
            fisio_informe i
        INNER JOIN 
            fisio_servicio ser ON ser.id = i.servicio_id
        INNER JOIN 
            fisio_profesional p ON p.id = i.profesional_id
        WHERE 
            i.estado_prof IN ('P', 'Pendiente')
            {filtros.replace('fecha', 'fecha_informe').format(table='i')}
        
        UNION ALL
        
        SELECT 
            sd.fecha AS fecha,
            sd.observaciones AS descripcion,
            ser.nombre AS servicio,
            p.nombre || ' ' || p.apellido AS profesional,
            ser.monto * 0.7 AS monto,
            'Sesión' as tipo
        FROM 
            fisio_sesiondetalle sd
        INNER JOIN 
            fisio_sesiones s ON s.id = sd.sesion_id
        INNER JOIN 
            fisio_consulta c ON c.id = s.consulta_id
        INNER JOIN 
            fisio_servicio ser ON ser.id = s.servicio_id
        INNER JOIN 
            fisio_profesional p ON p.id = c.profesional_id
        WHERE 
            sd.estado_prof IN ('P', 'Pendiente')
            {filtros.format(table='sd')}
        ORDER BY fecha DESC
        """

        # Ejecutar la consulta SQL
        with connection.cursor() as cursor:
            cursor.execute(sql, params * 3)  # Multiplicamos los parámetros por 3 debido al UNION ALL
            resultados = cursor.fetchall()

        # Convertir los resultados a un diccionario
        pagos = [
            {
                'fecha': row[0],
                'descripcion': row[1],
                'servicio': row[2],
                'profesional': row[3],
                'monto': row[4],
                'tipo': row[5]
            }
            for row in resultados
        ]

        profesionales = Profesional.objects.all()
        servicios = Servicio.objects.all()

        context = {
            "pagos": pagos, 
            "profesionales": profesionales, 
            "servicios": servicios,
            "filtros": {
                "profesional_id": profesional_id,
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta,
                "servicio_id": servicio_id
            }
        }

        return render(request, self.template_name, context)

    def post(self, request):
        seleccionados = request.POST.getlist('seleccionados')
        
        if seleccionados:
            with transaction.atomic():
                # Actualizar el estado a 'Cancelado'
                SesionDetalle.objects.filter(id__in=seleccionados).update(estado_prof='C')
                Consulta.objects.filter(id__in=seleccionados).update(estado_prof='C')
                Informe.objects.filter(id__in=seleccionados).update(estado_prof='C')

                # Generar PDF
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="pagos_profesional.pdf"'
                p = canvas.Canvas(response)
                p.drawString(100, 800, "Pagos al Profesional")
                y = 750
                for pago in seleccionados:
                    p.drawString(100, y, f"Fecha: {pago['fecha']}, Descripción: {pago['descripcion']}, Servicio: {pago['servicio']}, Monto: {pago['monto']}")
                    y -= 20
                p.showPage()
                p.save()

                # Registrar operación en flujo de caja
                for pago in seleccionados:
                    FlujoCaja.objects.create(
                        concepto='Salida de dinero',
                        monto=pago['monto'],
                        fecha=pago['fecha'],
                        descripcion=f"Pago al profesional {pago['profesional']} por {pago['descripcion']}"
                    )

                return response

        return redirect('pagos_profesionales')



# -------------------- Resumen General View --------------------

from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Cast
from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

class ResumenGeneralView(View):
    template_name = "resumen_gral.html"

    def get(self, request):
        profesionales = Consulta.objects.values("profesional__id", "profesional__nombre", "profesional__apellido").distinct()
        servicios = Servicio.objects.all()
        return render(request, self.template_name, {"profesionales": profesionales, "servicios": servicios})

    def post(self, request):
        profesional_id = request.POST.get("profesional")
        fecha_desde = request.POST.get("fecha_desde")
        fecha_hasta = request.POST.get("fecha_hasta")
        servicio_id = request.POST.get("servicio")

        # Filtrar consultas, informes y sesiones
        consultas = Consulta.objects.filter(estado_pago="C", estado_prof="C")
        informes = Informe.objects.filter(estado_pago="C", estado_prof="C")
        sesiones = SesionDetalle.objects.filter(estado_pago="C", estado_prof="C")

        if profesional_id:
            consultas = consultas.filter(profesional__id=profesional_id)
            informes = informes.filter(profesional__id=profesional_id)
            sesiones = sesiones.filter(sesion__consulta__profesional__id=profesional_id)
        if fecha_desde and fecha_hasta:
            consultas = consultas.filter(fecha__range=[fecha_desde, fecha_hasta])
            informes = informes.filter(fecha_informe__range=[fecha_desde, fecha_hasta])
            sesiones = sesiones.filter(fecha__range=[fecha_desde, fecha_hasta])
        if servicio_id:
            consultas = consultas.filter(servicio__id=servicio_id)
            informes = informes.filter(servicio__id=servicio_id)
            sesiones = sesiones.filter(sesion__servicio__id=servicio_id)

        # Calcular la utilidad por profesional
        consultas = consultas.values("profesional__nombre", "profesional__apellido").annotate(
            total_cobrado=Sum(F('servicio__monto')),
            total_pagado=Sum(F('servicio__monto')) * Decimal('0.3'),
            utilidad=Sum(F('servicio__monto')) - (Sum(F('servicio__monto')) * Decimal('0.3'))
        ).annotate(
            total_cobrado=Cast('total_cobrado', DecimalField(max_digits=10, decimal_places=0)),
            total_pagado=Cast('total_pagado', DecimalField(max_digits=10, decimal_places=0)),
            utilidad=Cast('utilidad', DecimalField(max_digits=10, decimal_places=0))
        )

        informes = informes.values("profesional__nombre", "profesional__apellido").annotate(
            total_cobrado=Sum(F('servicio__monto')),
            total_pagado=Sum(F('servicio__monto')) * Decimal('0.3'),
            utilidad=Sum(F('servicio__monto')) - (Sum(F('servicio__monto')) * Decimal('0.3'))
        ).annotate(
            total_cobrado=Cast('total_cobrado', DecimalField(max_digits=10, decimal_places=0)),
            total_pagado=Cast('total_pagado', DecimalField(max_digits=10, decimal_places=0)),
            utilidad=Cast('utilidad', DecimalField(max_digits=10, decimal_places=0))
        )

        sesiones = sesiones.values("sesion__consulta__profesional__nombre", "sesion__consulta__profesional__apellido").annotate(
            total_cobrado=Sum(F('sesion__servicio__monto')),
            total_pagado=Sum(F('sesion__servicio__monto')) * Decimal('0.3'),
            utilidad=Sum(F('sesion__servicio__monto')) - (Sum(F('sesion__servicio__monto')) * Decimal('0.3'))
        ).annotate(
            total_cobrado=Cast('total_cobrado', DecimalField(max_digits=10, decimal_places=0)),
            total_pagado=Cast('total_pagado', DecimalField(max_digits=10, decimal_places=0)),
            utilidad=Cast('utilidad', DecimalField(max_digits=10, decimal_places=0))
        )

        # Combinar los resultados
        resumen = list(consultas) + list(informes) + list(sesiones)

        # Generar PDF si se solicita
        if 'generar_pdf' in request.POST:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="resumen_general.pdf"'
            p = canvas.Canvas(response, pagesize=A4)
            width, height = A4
            
            # Encabezado
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, height - 50, "FISIOEMA")
            p.setFont("Helvetica", 12)
            p.drawString(width - 200, height - 50, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
            p.drawString(width - 200, height - 70, f"Usuario: {request.user.username}")
            p.line(50, height - 90, width - 50, height - 90)

            # Contenido
            y = height - 110
            total_cobrado_general = 0
            total_pagado_general = 0
            total_utilidad_general = 0
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y, "Profesional | Total Cobrado | Total Pagado | Utilidad")
            y -= 20
            p.setFont("Helvetica", 10)

            for item in resumen:
                p.drawString(50, y, f"{item['profesional__nombre']} {item['profesional__apellido']} | {item['total_cobrado']} | {item['total_pagado']} | {item['utilidad']}")
                total_cobrado_general += item['total_cobrado']
                total_pagado_general += item['total_pagado']
                total_utilidad_general += item['utilidad']
                y -= 20
                if y < 100:
                    p.showPage()
                    y = height - 100

            # Banda de totales
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y, f"Total Cobrado: {total_cobrado_general} | Total Pagado: {total_pagado_general} | Utilidad: {total_utilidad_general}")

            # Pie de página
            p.setFont("Helvetica", 12)
            p.drawString(50, 30, "FISIOEMA")
            p.line(50, 40, width - 50, 40)
            p.showPage()
            p.save()
            return response

        return render(request, self.template_name, {"resumen": resumen})

# -------------------- Flujo de Caja View --------------------
class FlujoCajaView(View):
    template_name = "flujo_caja_form.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        persona = request.POST.get("persona")
        monto = request.POST.get("monto")
        tipo_pago = request.POST.get("tipo_pago")

        FlujoCaja.objects.create(
            persona=persona,
            fecha=request.POST.get("fecha"),
            monto=monto,
            tipo_operacion="R",  # Recibo
            medio_pago=tipo_pago,
        )

        # Actualizar estados de las consultas seleccionadas
        consulta_ids = request.POST.getlist("consulta_ids")
        Consulta.objects.filter(id__in=consulta_ids).update(estado_pago="C")

        # Generar PDF
        pdf_data = {
            "fecha_operacion": request.POST.get("fecha"),
            "persona": persona,
            "concepto": "Recibo",
            "monto": monto,
            "tipo_pago": tipo_pago,
        }
        # pdf = generate_pdf(pdf_data)

        # return HttpResponse(pdf, content_type="application/pdf")

