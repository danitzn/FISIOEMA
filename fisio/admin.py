from django.contrib import admin

from fisio.models import Agendamiento, Area, Banco, DatosFactura, Descuento, Paciente, Perfil, Profesional, Servicio, TipoDescuento, Transaccion, TipoProfesionalArea, HorarioAtencion
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