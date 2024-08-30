# urls.py
from django.urls import path
from fisio.views import (
    PacienteListView, PacienteDetailView, PacienteCreateView,
    PacienteUpdateView, PacienteDeleteView,
    ProfesionalListView, ProfesionalDetailView, ProfesionalCreateView,
    ProfesionalUpdateView, ProfesionalDeleteView,
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
]
