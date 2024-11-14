# urls.py
from django import views
from django.urls import path
from django.contrib import admin
from fisio.views import (
    AgendamientoCreateProfView, AgendamientoCreateView, AgendamientoDeleteProfView, AgendamientoDeleteView, AgendamientoDetailProfView, AgendamientoDetailView, AgendamientoListProfView, AgendamientoListView, AgendamientoUpdateProfView, AgendamientoUpdateView, AreaCreateView, AreaDeleteView, AreaDetailProfView, AreaDetailView, AreaListProfView, AreaListView, AreaUpdateView, ConfirmacionAgendamientoProfView, ConfirmacionAgendamientoView, FlujoCajaListView, HorarioAtencionCreateView, HorarioAtencionDetailPacView, HorarioAtencionDetailProfView, HorarioAtencionDetailView, HorarioAtencionDeleteView, HorarioAtencionListPacView, HorarioAtencionListProfView, HorarioAtencionListView, HorarioAtencionUpdateView, PacienteDetailPacView, PacienteDetailProfView, PacienteListProfView, PacienteListView, PacienteDetailView, PacienteCreateView, PacienteUpdateProfView,
    PacienteUpdateView, PacienteDeleteView, ProfesionalDetailPacView, ProfesionalDetailProfView, ProfesionalListPacView, ProfesionalListProfView,
    ProfesionalListView, ProfesionalDetailView, ProfesionalCreateView, 
    ProfesionalUpdateView, ProfesionalDeleteView, ServicioCreateView, ServicioDeleteView, ServicioDetailPacView, ServicioDetailView, ServicioListPacView, ServicioListView, ServicioUpdateView, buscar_consultas_por_ci, cobrar_consulta, dashboard_view, generar_consulta, home,registro,login_view, calendario
)

urlpatterns = [
    #areas y servicios - Perfil Admin URLs
    path('areas/', AreaListView.as_view(), name='area_list'),
    path('areas/<int:pk>/', AreaDetailView.as_view(), name='area_detail'),
    path('areas/nuevo/', AreaCreateView.as_view(), name='area_create'),
    path('areas/<int:pk>/editar/', AreaUpdateView.as_view(), name='area_update'),
    path('areas/<int:pk>/eliminar/', AreaDeleteView.as_view(), name='area_confirm_delete'),
    path('servicios/', ServicioListView.as_view(), name='servicio_list'),
    path('servicios/<int:pk>/', ServicioDetailView.as_view(), name='servicio_detail'),
    path('servicios/nuevo/', ServicioCreateView.as_view(), name='servicio_form'),
    path('servicios/<int:pk>/editar/', ServicioUpdateView.as_view(), name='servicio_update'),
    path('servicios/<int:pk>/eliminar/', ServicioDeleteView.as_view(), name='servicio_confirm_delete'),

    #areas - Perfil Profesional URLs
    path('areasp/', AreaListProfView.as_view(), name='area_list_prof'),
    path('areasp/<int:pk>/', AreaDetailProfView.as_view(), name='area_detail_prof'),

    #servicios - Perfil Paciente URLs
    path('serviciospac/', ServicioListPacView.as_view(), name='servicio_list_paciente'),
    path('serviciospac/<int:pk>/', ServicioDetailPacView.as_view(), name='servicio_detail_paciente'),
    
    #horarios de atencion - Perfil Admin 
    path('horarios/', HorarioAtencionListView.as_view(), name='horario_list'),
    path('horarios/<int:pk>/', HorarioAtencionDetailView.as_view(), name='horario_detail'),
    path('horarios/nuevo/', HorarioAtencionCreateView.as_view(), name='horario_create'),
    path('horarios/<int:pk>/editar/', HorarioAtencionUpdateView.as_view(), name='horario_update'),
    path('horarios/<int:pk>/eliminar/', HorarioAtencionDeleteView.as_view(), name='horario_delete'),
    path('calendario_admin/',calendario, name='calendario_admin'),
    
    #horarios de atencion - Perfil Profesional
    path('horariosp/', HorarioAtencionListProfView.as_view(), name='horario_list_prof'),
    path('horariosp/<int:pk>/', HorarioAtencionDetailProfView.as_view(), name='horario_detail_prof'),
    path('calendario_admin/',calendario, name='calendario_admin'),
    
    #horarios de atencion - Perfil Paciente
    path('horariospac/', HorarioAtencionListPacView.as_view(), name='horario_list_paciente'),
    path('horariospac/<int:pk>/', HorarioAtencionDetailPacView.as_view(), name='horario_detail_paciente'),
    path('calendario_admin/',calendario, name='calendario_admin'),

    # Paciente - Perfil Admin URLs
    path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/<int:pk>/', PacienteDetailView.as_view(), name='paciente_detail'),
    path('pacientes/nuevo/', PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/<int:pk>/editar/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/eliminar/', PacienteDeleteView.as_view(), name='paciente_delete'),

    # Paciente - Perfil Profesional URLs
    path('pacientesp/', PacienteListProfView.as_view(), name='paciente_list_prof'),
    path('pacientesp/<int:pk>/', PacienteDetailProfView.as_view(), name='paciente_detail_prof'),
    path('pacientesp/<int:pk>/editar/', PacienteUpdateProfView.as_view(), name='paciente_update_prof'),

    # Paciente - Perfil Paciente URLs
    path('pacientespac/<int:pk>/', PacienteDetailPacView.as_view(), name='paciente_detail_paciente'),

    # Profesional - Perfil Admin URLs
    path('profesionales/', ProfesionalListView.as_view(), name='profesional_list'),
    path('profesionales/<int:pk>/', ProfesionalDetailView.as_view(), name='profesional_detail'),
    path('profesionales/nuevo/', ProfesionalCreateView.as_view(), name='profesional_create'),
    path('profesionales/<int:pk>/editar/', ProfesionalUpdateView.as_view(), name='profesional_update'),
    path('profesionales/<int:pk>/eliminar/', ProfesionalDeleteView.as_view(), name='profesional_delete'),
    
    # Profesional - Perfil Profesional URLs
    path('profesionalesp/', ProfesionalListProfView.as_view(), name='profesional_list_prof'),
    path('profesionalesp/<int:pk>/', ProfesionalDetailProfView.as_view(), name='profesional_detail_prof'),
    
    # Profesional - Perfil Profesional URLs
    path('profesionalespac/', ProfesionalListPacView.as_view(), name='profesional_list_paciente'),
    path('profesionalespac/<int:pk>/', ProfesionalDetailPacView.as_view(), name='profesional_detail_paciente'),

    #Agendamiento - Perfil Admin URLs
    path('agendamientos/', AgendamientoListView.as_view(), name='agendamiento_list'),
    path('agendamientos/<int:pk>/', AgendamientoDetailView.as_view(), name='agendamiento_detail'),
    path('agendamientos/nuevo/', AgendamientoCreateView.as_view(), name='agendamiento_create'),
    path('agendamientos/<int:pk>/editar/', AgendamientoUpdateView.as_view(), name='agendamiento_update'),
    path('agendamientos/confirmacion/', ConfirmacionAgendamientoView.as_view(), name='confirmacion_agendamiento'),
    path('agendamientos/eliminar/<int:pk>/', AgendamientoDeleteView.as_view(), name='agendamiento_delete'),
    path('calendario_admin/',calendario, name='calendario_admin'),
    path('generar_consulta/<int:agendamiento_id>/', generar_consulta, name='generar_consulta'),

    #Agendamiento - Perfil Profesional URLs 
    path('agendamientosp/', AgendamientoListProfView.as_view(), name='agendamiento_list_prof'),
    path('agendamientosp/<int:pk>/', AgendamientoDetailProfView.as_view(), name='agendamiento_detail_prof'),
    path('agendamientosp/nuevo/', AgendamientoCreateProfView.as_view(), name='agendamiento_create_prof'),
    path('agendamientosp/<int:pk>/editar/', AgendamientoUpdateProfView.as_view(), name='agendamiento_update_prof'),
    path('agendamientosp/confirmacion/', ConfirmacionAgendamientoProfView.as_view(), name='confirmacion_agendamiento_prof'),
    path('agendamientosp/eliminar/<int:pk>/', AgendamientoDeleteProfView.as_view(), name='agendamiento_delete_prof'),
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

    #cobros, consultas
    path("buscar-consultas/", buscar_consultas_por_ci, name="buscar_consultas_por_ci"),
    path("cobrar-consulta/<int:consulta_id>/", cobrar_consulta, name="cobrar_consulta"),
    path("cobrar-consulta/<int:consulta_id>/", cobrar_consulta, name="cobrar_consulta"),
    path('flujo_caja_list/', FlujoCajaListView.as_view(), name='flujo_caja_list'),
    
    
]

