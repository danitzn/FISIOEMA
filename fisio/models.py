from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, time



class Direccion(models.Model):
    domicilio = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.domicilio}, {self.ciudad}, {self.estado}"



class Responsable(models.Model):
    nrodocumento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    celular = models.CharField(max_length=20)
    mail = models.EmailField()
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Paciente(models.Model):
    nrodocumento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    celular = models.CharField(max_length=20)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    diagnostico_medico = models.CharField(max_length=200)
    medico_tratante = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    fecha_registro = models.DateField(auto_now_add=True)
    mail = models.EmailField(unique=True)  # Asegúrate de que sea único en la base de datos
    responsable = models.ForeignKey('Responsable', on_delete=models.CASCADE, related_name='pacientes', null=True, blank=True)

    @property
    def edad(self):
        """Calcula la edad del paciente en función de su fecha de nacimiento."""
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    def es_mayor_de_edad(self):
        """Devuelve True si el paciente es mayor de edad, False si no lo es."""
        return self.edad >= 18

    def clean(self):
        """Realiza las validaciones del modelo antes de guardar."""
        # Verifica que los pacientes menores de edad tengan un responsable
        if not self.es_mayor_de_edad() and not self.responsable:
            raise ValidationError("Los pacientes menores de edad deben tener un responsable.")
        
        # Verifica si el número de documento ya está registrado
        if Paciente.objects.filter(nrodocumento=self.nrodocumento).exclude(pk=self.pk).exists():
            raise ValidationError('El número de documento ya está registrado.')

        # Verifica si el correo electrónico ya está registrado
        if Paciente.objects.filter(mail=self.mail).exclude(pk=self.pk).exists():
            raise ValidationError('El correo electrónico ya está registrado.')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    

#datos del profesional
class Profesional(models.Model):
    nrodocumento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    celular = models.CharField(max_length=20)
    correo = models.EmailField()
    fecha_registro = models.DateField(auto_now_add=True)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    activo = models.BooleanField(default=True)
    responsable_area = models.ForeignKey('Area', on_delete=models.CASCADE, related_name='profesionales', null=True, blank=True)
    
    

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    

#datos del horario de atencion de los profesionales

class HorarioAtencion(models.Model):
    TURNOS_CHOICES = [
        ('M', 'Mañana (07:00 - 10:00)'),
        ('S', 'Siesta (10:00 - 13:00)'),
        ('T', 'Tarde (14:00 - 18:00)'),
    ]

    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='horarios_atencion')
    fecha = models.DateField()  # Cambiamos a DateField para incluir fechas
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    idturno = models.CharField(max_length=1, choices=TURNOS_CHOICES, blank=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='horarios_atencion')

    def __str__(self):
        return f"{self.fecha} ({self.hora_inicio} - {self.hora_fin}) - {self.servicio}"

    def save(self, *args, **kwargs):
        """ Sobreescribe el método save para realizar las validaciones antes de guardar """
        self.asigna_turno()  # Llamamos al método antes de guardar
        super().save(*args, **kwargs)

    def clean(self):
        """ Método clean para validaciones personalizadas """
        # 1. Validar que la hora de inicio sea menor que la hora de fin
        if self.hora_inicio >= self.hora_fin:
            raise ValueError("La hora de inicio debe ser menor que la hora de fin.")
        
        # 2. Validar que la fecha no sea menor a hoy
        if self.fecha< date.today():
            raise ValueError("La fecha no puede ser menor que la fecha de hoy.")
        
        # 3. Validar que el día no sea domingo
        if self.fecha.weekday() == 6:  # 6 representa el domingo en Python
            raise ValueError("No se pueden agendar turnos los días domingo.")
        

    def asigna_turno(self):
        """ Asigna el turno basado en la hora de inicio y fin """
        if time(7, 0) <= self.hora_inicio < time(10, 0) and self.hora_fin <= time(10, 0):
            self.idturno = 'M'  # Mañana
        elif time(10, 0) <= self.hora_inicio < time(13, 0) and self.hora_fin <= time(13, 0):
            self.idturno = 'S'  # Siesta
        elif time(14, 0) <= self.hora_inicio < time(18, 0) and self.hora_fin <= time(18, 0):
            self.idturno = 'T'  # Tarde
        else:
            raise ValueError("El horario debe estar entre las 07:00 y las 18:00 horas.")
        


class Agendamiento(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente de Confirmación'),
        ('confirmado', 'Confirmado'),
        ('reprogramado', 'Reprogramado'),
        ('cancelado_paciente', 'Cancelado por el Paciente'),
        ('cancelado_profesional', 'Cancelado por el Profesional'),
        ('no_asistido', 'No Asistido'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamientos')
    fecha = models.DateField()
    hora = models.TimeField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='agendamientos')
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='agendamientos')
    estado = models.CharField(max_length=30, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.paciente} ({self.estado})"
    
    def clean(self):
        # Validar si ya existe un agendamiento en el mismo horario para el mismo profesional y servicio.
        agendamientos_conflictivos = Agendamiento.objects.filter(
            profesional=self.profesional,
            servicio=self.servicio,
            fecha=self.fecha,
            hora=self.hora
        ).exclude(id=self.id)  # Excluir el agendamiento actual si se está editando

        if agendamientos_conflictivos.exists():
            raise ValidationError("Este turno ya está reservado para este profesional.")

    def __str__(self):
        return f"{self.profesional} - {self.servicio} ({self.fecha} a las {self.hora})"

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

# class Tarifa(models.Model):
#     servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
#     nombre = models.CharField(max_length=50)
#     monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Cobro(models.Model):
    # tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
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
        return f'{self.user.username}' 
        # - {self.get_tipo_display()}'


class Area(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Consulta(models.Model):
    ESTADO_CHOICES = [
        ('C', 'Cancelado'),
        ('P', 'Pendiente'),
        ('PP', 'Pago Parcial'),
    ]
    estado_pago = models.CharField(max_length=2, choices=ESTADO_CHOICES, default='P')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    fecha = models.DateField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    hora = models.TimeField()
    motivo_consulta = models.TextField()
    diagnostico = models.TextField()
    tiene_sesiones = models.BooleanField(default=False)


    def __str__(self):
        return f"Consulta de {self.paciente} con {self.profesional} el {self.fecha} a las {self.hora}"

class Sesiones (models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    cantidad_sesiones = models.IntegerField()
    cantidad_realizadas = models.IntegerField(default =0)
    finalizado = models.BooleanField(default=False)
    


class SesionDetalle (models.Model):
    sesion = models.ForeignKey(Sesiones, on_delete=models.CASCADE)
    numero_sesion = models.IntegerField()
    fecha = models.DateField(default = date.today)
    hora = models.TimeField(default = time)
    observaciones = models.TextField()
    estado = models.CharField(max_length=20, choices=[('A', 'Asistido'), ('N', 'No Asistido')])
    estado_pago = models.CharField(max_length=20, choices=[
        ('C', 'Cancelado'),
        ('P', 'Pendiente'),
        ('PP', 'Pago Parcial'),
    ])


class FlujoCaja(models.Model):
    persona = models.CharField(max_length=20, null=True, blank=True)  # CI de paciente, profesional, o ninguno
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=0)
    TIPO_OPERACION_CHOICES = [
        ('R', 'Recibo (Entrada)'),
        ('P', 'Pago (Salida)'),
    ]
    tipo_operacion = models.CharField(max_length=1, choices=TIPO_OPERACION_CHOICES)
    MEDIO_PAGO_CHOICES = [
        ('E', 'Efectivo'),
        ('T', 'Transferencia'),
        ('C', 'Cheque'),
        ('O', 'Otros'),
    ]
    medio_pago = models.CharField(max_length=1, choices=MEDIO_PAGO_CHOICES)

    def __str__(self):
        return f"{self.persona} - {self.tipo_operacion} - {self.monto}"