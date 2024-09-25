from django.contrib import admin

from fisio.models import Agendamiento, Banco, DatosFactura, Descuento, Paciente, Perfil, Profesional, Servicio, TipoDescuento, Transaccion, TipoProfesionalArea
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