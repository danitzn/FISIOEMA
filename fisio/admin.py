from django.contrib import admin

from fisio.models import Banco, DatosFactura, Descuento, Paciente, Perfil, Profesional, TipoDescuento, Transaccion

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Profesional)
admin.site.register(Perfil)
admin.site.register(Banco)
admin.site.register(Transaccion)
admin.site.register(DatosFactura)
admin.site.register(TipoDescuento)
admin.site.register(Descuento)
