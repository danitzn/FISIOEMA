# urls.py
from django import views
from django.urls import path
from django.contrib import admin
from fisio.views import (
    AgendamientoCreateView, AgendamientoDeleteView, AgendamientoDetailView, AgendamientoListView, AgendamientoUpdateView, AreaCreateView, AreaDeleteView, AreaDetailView, AreaListView, AreaUpdateView, ConfirmacionAgendamientoView, HorarioAtencionCreateView, HorarioAtencionDeleteView, HorarioAtencionListView, HorarioAtencionUpdateView, PacienteListView, PacienteDetailView, PacienteCreateView,
    PacienteUpdateView, PacienteDeleteView,
    ProfesionalListView, ProfesionalDetailView, ProfesionalCreateView,
    ProfesionalUpdateView, ProfesionalDeleteView, ServicioCreateView, ServicioDeleteView, ServicioDetailView, ServicioListView, ServicioUpdateView, dashboard_view, generar_consulta, home,registro,login_view, calendario
)

urlpatterns = [
    #areas y servicios URLs
    path('areas/', AreaListView.as_view(), name='area_list'),
    path('areas/<int:pk>/', AreaDetailView.as_view(), name='area_detail'),
    path('areas/nuevo/', AreaCreateView.as_view(), name='area_create'),
    path('areas/<int:pk>/editar/', AreaUpdateView.as_view(), name='area_update'),
    path('areas/<int:pk>/eliminar/', AreaDeleteView.as_view(), name='area_delete'),
    path('servicios/', ServicioListView.as_view(), name='servicio_list'),
    path('servicios/<int:pk>/', ServicioDetailView.as_view(), name='servicio_detail'),
    path('servicios/nuevo/', ServicioCreateView.as_view(), name='servicio_create'),
    path('servicios/<int:pk>/editar/', ServicioUpdateView.as_view(), name='servicio_update'),
    path('servicios/<int:pk>/eliminar/', ServicioDeleteView.as_view(), name='servicio_delete'),

    
    #horarios de atencion
    path('horarios/', HorarioAtencionListView.as_view(), name='horario_list'),
    path('horarios/<int:pk>/', HorarioAtencionListView.as_view(), name='horario_detail'),
    path('horarios/nuevo/', HorarioAtencionCreateView.as_view(), name='horario_create'),
    path('horarios/<int:pk>/editar/', HorarioAtencionUpdateView.as_view(), name='horario_update'),
    path('horarios/<int:pk>/eliminar/', HorarioAtencionDeleteView.as_view(), name='horario_delete'),


    # Paciente URLs
    path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/<int:pk>/', PacienteDetailView.as_view(), name='paciente_detail'),
    path('pacientes/nuevo/', PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/<int:pk>/editar/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/eliminar/', PacienteDeleteView.as_view(), name='paciente_delete'),

    # Profesional URLs
    path('profesionales/', ProfesionalListView.as_view(), name='profesional_list'),
    path('profesionales/<int:pk>/', ProfesionalDetailView.as_view(), name='profesional_detail'),
    path('profesionales/nuevo/', ProfesionalCreateView.as_view(), name='profesional_create'),
    path('profesionales/<int:pk>/editar/', ProfesionalUpdateView.as_view(), name='profesional_update'),
    path('profesionales/<int:pk>/eliminar/', ProfesionalDeleteView.as_view(), name='profesional_delete'),

    #Agendamiento URLs
    path('agendamientos/', AgendamientoListView.as_view(), name='agendamiento_list'),
    path('agendamientos/<int:pk>/', AgendamientoDetailView.as_view(), name='agendamiento_detail'),
    path('agendamientos/nuevo/', AgendamientoCreateView.as_view(), name='agendamiento_create'),
    path('agendamientos/<int:pk>/editar/', AgendamientoUpdateView.as_view(), name='agendamiento_update'),
    path('agendamientos/confirmacion/', ConfirmacionAgendamientoView.as_view(), name='confirmacion_agendamiento'),
    path('agendamientos/eliminar/<int:pk>/', AgendamientoDeleteView.as_view(), name='agendamiento_delete'),
    path('calendario_admin/',calendario, name='calendario_admin'),
    path('generar_consulta/<int:agendamiento_id>/', generar_consulta, name='generar_consulta'),

    # Usuario URLs
    path('admin/', admin.site.urls, name='admin'),
    path('registro/', registro, name='registro'),
    # path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', home, name='home'),  # Página de inicio (login)
    path('login/', home, name='login'),
    path('logout/', home, name='logout'),
    
]

