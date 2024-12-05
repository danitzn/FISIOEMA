# views.py
import json
from django.http import HttpResponse
from django.utils import timezone  
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Agendamiento, Consulta, FlujoCaja, HorarioAtencion, Paciente, Profesional, Servicio, Area
from .forms import AgendamientoForm, PacienteForm, ProfesionalForm, RegistroForm, SesionesForm
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import requires_csrf_token
from django.db.models import Sum
from reportlab.pdfgen import canvas
import csv

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
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        # Capturar el parámetro de búsqueda del nombre del área
        nombre_area = self.request.GET.get('nombre', '')

        # Filtrar si el parámetro no está vacío
        if nombre_area:
            queryset = queryset.filter(nombre__icontains=nombre_area)

        return queryset

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
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        servicio = self.request.GET.get('servicio', '')

        if servicio:
            queryset = queryset.filter(nombre__icontains=servicio)

        return queryset

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
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.GET.get('nombre', '')
        apellido = self.request.GET.get('apellido', '')
        nrodocumento = self.request.GET.get('nrodocumento', '')

        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if apellido:
            queryset = queryset.filter(apellido__icontains=apellido)
        if nrodocumento:
            queryset = queryset.filter(nrodocumento__icontains=nrodocumento)

        return queryset

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
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.GET.get('nombre', '')
        apellidos = self.request.GET.get('apellidos', '')
        especialidad = self.request.GET.get('especialidad', '')

        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if apellidos:
            queryset = queryset.filter(apellidos__icontains=apellidos)
        if especialidad:
            queryset = queryset.filter(responsable_area__icontains=especialidad)

        return queryset

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

# Profesional - PERFIL PROFESIONAL Views
class ProfesionalListProfView(ListView):
    model = Profesional
    template_name = 'profesional_list_prof.html'
    context_object_name = 'profesionalesp'

class ProfesionalDetailProfView(DetailView):
    model = Profesional
    template_name = 'profesional_detail_prof.html'
    context_object_name = 'profesionalp'

# Profesional - PERFIL Paciente Views
class ProfesionalListPacView(ListView):
    model = Profesional
    template_name = 'profesional_list_paciente.html'
    context_object_name = 'profesionalespac'

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

# Agendamiento - Perfil Admin

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
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()  # Asegúrate de tener esta línea correctamente indentada

        # Obtener parámetros de filtro
        profesional = self.request.GET.get('profesional', '')
        servicio = self.request.GET.get('servicio', '')
        turno = self.request.GET.get('turno', '')

        # Aplicar filtros
        if profesional:
            queryset = queryset.filter(profesional__nombre__icontains=profesional)  # Filtrar por nombre del profesional
        if servicio:
            queryset = queryset.filter(servicio__nombre__icontains=servicio)  # Filtrar por nombre del servicio
        if turno:
            queryset = queryset.filter(hora__icontains=turno)  # Filtrar por hora del turno

        return queryset

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
    paginate_by = 5

    def get_queryset(self):
        # Obtener el queryset inicial
        queryset = super().get_queryset()

        # Capturar parámetros de búsqueda de la URL
        profesional = self.request.GET.get('profesional', '')
        servicio = self.request.GET.get('servicio', '')
        turno = self.request.GET.get('turno', '')

        # Filtrar el queryset si los parámetros no están vacíos
        if profesional:
            queryset = queryset.filter(profesional__nombre__icontains=profesional)
        if servicio:
            queryset = queryset.filter(servicio__nombre__icontains=servicio)
        if turno:
            queryset = queryset.filter(idturno=turno)

        # Añadir ordenamiento explícito
        queryset = queryset.order_by('fecha', 'hora_inicio')

        return queryset

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


#calendario
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
    eventos_json = json.dumps(eventos) if eventos else '[]'
    return render(request, 'dashboard_administrador.html', {
        'eventos_json': eventos_json
    })
class FlujoCajaListView(ListView):
    model = FlujoCaja
    template_name = 'flujo_caja_list.html'
    context_object_name = 'flujo_dinero'

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
    if agendamiento.estado == 'en_curso':
        return redirect('calendario_admin')  # Redirigir al calendario si el agendamiento está en curso

    sesiones_form = None
    if request.method == 'POST':
        motivo_consulta = request.POST.get('motivo_consulta')
        diagnostico = request.POST.get('diagnostico')
        fecha_consulta = request.POST.get('fecha_consulta')
        tiene_sesiones = request.POST.get('tiene_sesiones') == 'on'

        # Crear consulta
        nueva_consulta = Consulta.objects.create(
            paciente=agendamiento.paciente,
            profesional=agendamiento.profesional,
            fecha=fecha_consulta,
            servicio=agendamiento.servicio,
            hora=agendamiento.hora,
            motivo_consulta=motivo_consulta,
            diagnostico=diagnostico,
            tiene_sesiones=tiene_sesiones
        )

        # Si tiene sesiones, manejar el formulario de sesiones
        if tiene_sesiones:
            sesiones_form = SesionesForm(request.POST)
            if sesiones_form.is_valid():
                nueva_sesion = sesiones_form.save(commit=False)
                nueva_sesion.paciente = nueva_consulta.paciente
                nueva_sesion.consulta = nueva_consulta
                nueva_sesion.servicio = nueva_consulta.servicio
                nueva_sesion.save()

        # Actualizar estado del agendamiento
        agendamiento.estado = 'finalizado'
        agendamiento.save()

        return redirect('calendario_admin')

    # Inicializar el formulario de sesiones solo si es necesario
    if not sesiones_form:
        sesiones_form = SesionesForm()

    return render(request, 'generar_consulta.html', {
        'agendamiento': agendamiento,
        'sesiones_form': sesiones_form
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

# Función para generar el PDF
def exportar_pdf(consultas):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_consultas.pdf"'

    c = canvas.Canvas(response)
    c.drawString(100, 800, "Reporte de Consultas")
    y = 750
    c.drawString(50, y, "Nombre de Paciente")
    c.drawString(250, y, "Motivo de la Consulta")
    c.drawString(450, y, "Diagnóstico")
    y -= 30

    for consulta in consultas:
        c.drawString(50, y, f"{consulta.paciente.nombre} {consulta.paciente.apellido}")
        c.drawString(250, y, consulta.motivo_consulta[:50])  # Limitar texto
        c.drawString(450, y, consulta.diagnostico[:50])  # Limitar texto
        y -= 30

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