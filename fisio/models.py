from django.db import models

class Direccion(models.Model):
    domicilio = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.domicilio}, {self.ciudad}, {self.estado}"

class Paciente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    celular = models.CharField(max_length=20)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    diagnostico_medico = models.CharField(max_length=200)
    medico_tratante = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Responsable(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    celular = models.CharField(max_length=20)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='responsables')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Servicio(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    

#datos del profesional
class Profesional(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    celular = models.CharField(max_length=20)
    correo = models.EmailField()
    fecha_registro = models.DateField(auto_now_add=True)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    tipo_profesional = models.ForeignKey('self',on_delete=models.CASCADE, related_name='profesionales')
    activo = models.BooleanField(default=True)
    responsable_area = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinados')
    

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
#datos del horario de atencion de los profesionales
class HorarioAtencion(models.Model):
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='horarios_atencion')
    dia = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.dia} ({self.hora_inicio}-{self.hora_fin})"
class Agendamiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamientos')
    fecha = models.DateField()
    hora = models.TimeField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='agendamientos')
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='agendamientos')
    estado = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.paciente}"

class Evaluacion(models.Model):
    agendamiento = models.ForeignKey(Agendamiento, on_delete=models.CASCADE, related_name='evaluaciones')
    resultado_clinico = models.TextField()

    def __str__(self):
        return f"Evaluación de {self.agendamiento}"

class Session(models.Model):
    agendamiento = models.ForeignKey(Agendamiento, on_delete=models.CASCADE, related_name='sessions')
    fecha = models.DateField()
    evolucion = models.CharField(max_length=200)

    def __str__(self):
        return f"Sesión del {self.fecha} - {self.agendamiento.paciente}"

class HistoriaMedico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historias_medicas')
    descripcion = models.CharField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True)
    informe = models.ForeignKey('Informe', on_delete=models.CASCADE)

    def __str__(self):
        return f"Historia Médica de {self.paciente} - {self.descripcion}"

class Informe(models.Model):
    fecha_informe = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f"Informe del {self.fecha_informe}"

class TipoInformeArea(models.Model):
    nombre = models.CharField(max_length=100)
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE, related_name='tipos_informe')

    def __str__(self):
        return self.nombre

class TipoProfesionalArea(models.Model):
    nombre = models.CharField(max_length=100)
    profesionales = models.ManyToManyField(Profesional, related_name='tipos_profesional')

    def __str__(self):
        return self.nombre

class Tarifa(models.Model):
    nombre = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Cobro(models.Model):
    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    fecha = models.DateField()

    def __str__(self):
        return f"Cobro de {self.tarifa.nombre} - {self.fecha}"

class CobroSeguroMedico(models.Model):
    cobro = models.ForeignKey(Cobro, on_delete=models.CASCADE)
    seguro_medico = models.ForeignKey('SeguroMedico', on_delete=models.CASCADE)

    def __str__(self):
        return f"Cobro de seguro médico {self.seguro_medico.nombre}"

class SeguroMedico(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Pago(models.Model):
    agendamiento = models.ForeignKey(Agendamiento, on_delete=models.CASCADE)
    honorario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Pago de {self.honorario} - {self.fecha}"

class Gasto(models.Model):
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_gasto = models.DateField()

    def __str__(self):
        return f"Gasto de {self.monto} - {self.fecha_gasto}"

class TipoGasto(models.Model):
    nombre = models.CharField(max_length=50)
    gastos = models.ManyToManyField(Gasto, related_name='tipos_gasto')

    def __str__(self):
        return self.nombre

class Horario(models.Model):
    dia_trabajo = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dia_trabajo

class DiasTrabajo(models.Model):
    dia = models.CharField(max_length=10)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dia} ({self.hora_inicio}-{self.hora_fin})"

class Banco(models.Model):
    nombre_banco = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_banco

class Transaccion(models.Model):
    numero_transaccion = models.CharField(max_length=50)
    fecha = models.DateField()
    tipo = models.CharField(max_length=50)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)

    def __str__(self):
        return f"Transacción {self.numero_transaccion} - {self.tipo}"

class DatosFactura(models.Model):
    razon_social = models.CharField(max_length=100)
    fecha_emision = models.DateField()
    detalle = models.TextField()

    def __str__(self):
        return self.razon_social

class TipoDescuento(models.Model):
    nombre = models.CharField(max_length=50)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre

class Descuento(models.Model):
    nombre = models.CharField(max_length=50)
    codigo_descuento = models.CharField(max_length=50)
    tipo_descuento = models.ForeignKey(TipoDescuento, on_delete=models.CASCADE)

    def __str__(self):
        return f"Descuento {self.nombre}"

class DatosCheque(models.Model):
    cheque = models.ForeignKey(Transaccion, on_delete=models.CASCADE)
    denominacion = models.CharField(max_length=100)
    fecha_emision = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f"Cheque {self.denominacion} - {self.fecha_emision}"

class PagoServicio(models.Model):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pago de {self.servicio.nombre} - {self.pago.fecha}"
from django.contrib.auth.models import User
from django.db import models

#perfiles de usuario

class Perfil(models.Model):
    USER_TYPES = (
        ('ADMINISTRADOR', 'Administrador'),
        ('PROFESIONAL', 'Profesional'),
        ('PACIENTE', 'Paciente'),
        ('ADMINISTRATIVO', 'Administrativo'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=USER_TYPES)
    nro_documento = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.get_tipo_display()}'
