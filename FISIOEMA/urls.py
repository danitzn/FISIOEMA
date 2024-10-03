# urls.py
from django import views
from django.urls import path
# from . import views
from django.contrib import admin
from fisio.views import (
    AgendamientoCreateView, AgendamientoDetailView, AgendamientoListView, ConfirmacionAgendamientoView, PacienteListView, PacienteDetailView, PacienteCreateView,
    PacienteUpdateView, PacienteDeleteView,
    ProfesionalListView, ProfesionalDetailView, ProfesionalCreateView,
    ProfesionalUpdateView, ProfesionalDeleteView, dashboard_view, home,registro,login_view,
)

urlpatterns = [
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

    # path('agendamientos/nuevo/', AgendamientoCreateView.as_view(), name='agendamiento_nuevo'),
    path('agendamientos/confirmacion/', ConfirmacionAgendamientoView.as_view(), name='confirmacion_agendamiento'),


    # Usuario URLs
    path('admin/', admin.site.urls, name='admin'),
    path('registro/', registro, name='registro'),
    # path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', home, name='home'),  # Página de inicio (login)
    path('login/', home, name='login'),
    
]

