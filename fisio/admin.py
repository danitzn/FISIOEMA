from django.contrib import admin

from fisio.models import Agendamiento, Area, Banco, Consulta, DatosFactura, Descuento, FlujoCaja, Informe, Paciente, Perfil, Profesional, Responsable, Servicio, SesionDetalle, Sesiones, TipoDescuento, Transaccion, TipoProfesionalArea, HorarioAtencion, FlujoCaja, Informe, Responsable
# Register your models here.
admin.site.register(Paciente)
admin.site.register(Profesional)
admin.site.register(Perfil)
admin.site.register(Banco)
admin.site.register(Agendamiento)
admin.site.register(Transaccion)
admin.site.register(DatosFactura)
admin.site.register(TipoDescuento)
admin.site.register(Descuento)
admin.site.register(TipoProfesionalArea)
admin.site.register(Servicio)
admin.site.register(Area)
admin.site.register(HorarioAtencion)
admin.site.register(Consulta)
admin.site.register(FlujoCaja)
admin.site.register(Informe)
admin.site.register(Sesiones)
admin.site.register(SesionDetalle)
admin.site.register(Responsable)