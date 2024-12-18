import re
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
    
    def clean(self):
        # Validar que el nrodocumento solo contenga números
        if not self.nrodocumento.isdigit():
            raise ValidationError({'nrodocumento': 'El número de documento debe contener solo números.'})

        # Validar que el nombre y apellido solo contengan letras
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", self.nombre):
            raise ValidationError({'nombre': 'El nombre debe contener solo letras.'})
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", self.apellido):
            raise ValidationError({'apellido': 'El apellido debe contener solo letras.'})

        # Validar que el celular solo contenga números
        if not self.celular.isdigit():
            raise ValidationError({'celular': 'El número de celular debe contener solo números.'})

        # Validar que el email tenga un formato correcto (esto ya lo hace EmailField, pero puedes agregar validaciones adicionales si es necesario)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.mail):
            raise ValidationError({'mail': 'El correo electrónico no es válido.'})
    

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
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None

    def es_mayor_de_edad(self):
        """Devuelve True si el paciente es mayor de edad, False si no lo es."""
        return self.edad is not None and self.edad >= 18

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

        # Validar que el nrodocumento solo contenga números
        if not self.nrodocumento.isdigit():
            raise ValidationError({'nrodocumento': 'El número de documento debe contener solo números.'})

        # Validar que el nombre y apellido solo contengan letras
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", self.nombre):
            raise ValidationError({'nombre': 'El nombre debe contener solo letras.'})
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", self.apellido):
            raise ValidationError({'apellido': 'El apellido debe contener solo letras.'})

        # Validar que el celular solo contenga números
        if not self.celular.isdigit():
            raise ValidationError({'celular': 'El número de celular debe contener solo números.'})

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
    registro_profesional = models.CharField(max_length=40)
    fecha_nacimiento = models.DateField()
    celular = models.CharField(max_length=20)
    correo = models.EmailField()
    fecha_registro = models.DateField(auto_now_add=True)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    activo = models.BooleanField(default=True)
    responsable_area = models.ForeignKey('Area', on_delete=models.CASCADE, related_name='profesionales', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    
    class Meta:
        ordering = ['apellidos', 'nombre']

    def clean(self):
        """ Método clean para validaciones personalizadas """
        try:
            # Validar que la fecha de nacimiento no sea en el futuro
            if self.fecha_nacimiento > date.today():
                raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
            
            # Validar que el número de documento solo contenga dígitos
            if not self.nrodocumento.isdigit():
                raise ValidationError("El número de documento debe contener solo dígitos.")
            
            # Validar que el celular solo contenga dígitos
            if not self.celular.isdigit():
                raise ValidationError("El número de celular debe contener solo dígitos.")
            
        except TypeError:
            raise ValidationError("Error en alguna entrada de dato. Favor corregir.")
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
        try:
            # 1. Validar que la hora de inicio sea menor que la hora de fin
            if self.hora_inicio >= self.hora_fin:
                raise ValidationError("La hora de inicio debe ser menor que la hora de fin.")
            
            # 2. Validar que la fecha no sea menor a hoy
            if self.fecha < date.today():
                raise ValidationError("La fecha no puede ser menor que la fecha de hoy.")
            
            # 3. Validar que el día no sea domingo
            if self.fecha.weekday() == 6:  # 6 representa el domingo en Python
                raise ValidationError("No se pueden agendar turnos los días domingo.")
            
            # Llamar a asigna_turno para validar el horario
            self.asigna_turno()
        except TypeError:
            raise ValidationError("Error en alguna entrada de dato. Favor corregir.")
    
    def asigna_turno(self):
        """ Asigna el turno basado en la hora de inicio y fin """
        if time(7, 0) <= self.hora_inicio < time(10, 0) and self.hora_fin <= time(10, 0):
            self.idturno = 'M'  # Mañana
        elif time(10, 0) <= self.hora_inicio < time(13, 0) and self.hora_fin <= time(13, 0):
            self.idturno = 'S'  # Siesta
        elif time(14, 0) <= self.hora_inicio < time(18, 0) and self.hora_fin <= time(18, 0):
            self.idturno = 'T'  # Tarde
        else:
            raise ValidationError("El horario debe estar entre las 07:00 y las 18:00 horas.")
        


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
    TIPO_CHOICES = [
        ('E', 'Evaluación'),
        ('S', 'Sesión'),
        ('I', 'Informe'),
    ]
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamientos')
    fecha = models.DateField()
    hora = models.TimeField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='agendamientos')
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='agendamientos')
    estado = models.CharField(max_length=30, choices=ESTADOS, default='pendiente')
    referencia_sesion = models.IntegerField(null=True, blank=True)

    def clean(self):
        super().clean()
        try:
            # 1. Verificar conflictos de agendamientos
            agendamientos_conflictivos = Agendamiento.objects.filter(
                profesional=self.profesional,
                servicio=self.servicio,
                fecha=self.fecha,
                hora=self.hora
            ).exclude(id=self.id)

            if agendamientos_conflictivos.exists():
                raise ValidationError("Este turno ya está reservado para este profesional.")

            # 2. Validar que el horario del agendamiento coincida con el horario de atención
            horario_atencion = HorarioAtencion.objects.filter(
                profesional=self.profesional,
                servicio=self.servicio,
                fecha=self.fecha,
                hora_inicio__lte=self.hora,
                hora_fin__gt=self.hora
            ).first()

            if not horario_atencion:
                raise ValidationError("El horario del agendamiento no coincide con el horario de atención del profesional.")

            # 3. Validar referencia_sesion para el tipo 'Sesión'
            if self.tipo == 'S':
                if not self.referencia_sesion:
                    raise ValidationError("Debe seleccionar una sesión de referencia para el tipo 'Sesión'.")
                
                sesion = Sesiones.validar_sesion(
                    referencia_sesion=self.referencia_sesion,
                    paciente=self.paciente,
                    servicio=self.servicio
                )
                if not sesion:
                    raise ValidationError("La sesión de referencia no es válida o ya finalizó.")

            # 4. Validar que la fecha no sea domingo
            if self.fecha.weekday() == 6:
                raise ValidationError("No se pueden agendar turnos los domingos.")
        
        except TypeError:
            raise ValidationError("Error en alguna entrada de dato. Favor corregir.")

    def __str__(self):
        return f"{self.tipo} | {self.paciente} | {self.fecha} {self.hora} | {self.estado}"



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
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)  
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)

    def __str__(self):
        return f"Informe de {self.paciente} por {self.profesional} el {self.fecha_informe}"
 

    

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

class Sesiones(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    cantidad_sesiones = models.IntegerField()
    cantidad_realizadas = models.IntegerField(default=0)
    finalizado = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.nombre}, {self.fecha_inicio}, {self.cantidad_sesiones}, {self.cantidad_realizadas}, {self.finalizado}"


    def save(self, *args, **kwargs):
        # Validación: cantidad_realizadas no puede exceder cantidad_sesiones
        if self.cantidad_realizadas > self.cantidad_sesiones:
            raise ValueError("La cantidad de sesiones realizadas no puede exceder el total de sesiones.")
        super().save(*args, **kwargs)

    @classmethod
    def validar_sesion(cls, referencia_sesion, paciente, servicio):
        """
        Valida si existe una sesión activa para un paciente y servicio específicos.
        """
        try:
            sesion = cls.objects.get(
                id=referencia_sesion,
                paciente=paciente,
                servicio=servicio,
                finalizado=False
            )
            return sesion  # Devuelve la sesión si es válida
        except cls.DoesNotExist:
            return None  # No se encontró una sesión válida

       
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

    def __str__(self):
        return f"{self.fecha}, {self.hora}, {self.observaciones}, {self.estado}, {self.estado_pago}"

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