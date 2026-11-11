from django.conf import settings
from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Herramienta(models.Model):
    ESTADO_BUENO = 'BUENO'
    ESTADO_REGULAR = 'REGULAR'
    ESTADO_REPARACION = 'REPARACION'
    ESTADOS = [
        (ESTADO_BUENO, 'Bueno'),
        (ESTADO_REGULAR, 'Regular'),
        (ESTADO_REPARACION, 'En reparación'),
    ]

    codigo = models.CharField(max_length=7, unique=True)
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='herramientas')
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ESTADO_BUENO)
    disponible = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Prestamo(models.Model):
    ESTADO_PENDIENTE = 'PENDIENTE'
    ESTADO_ACTIVO = 'ACTIVO'
    ESTADO_DEVUELTO = 'DEVUELTO'
    ESTADO_CANCELADO = 'CANCELADO'
    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_ACTIVO, 'Activo'),
        (ESTADO_DEVUELTO, 'Devuelto'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    socio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prestamos')
    herramienta = models.ForeignKey(Herramienta, on_delete=models.PROTECT, related_name='prestamos')
    fecha_solicitud = models.DateField(default=timezone.localdate)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ESTADO_PENDIENTE)

    class Meta:
        verbose_name = 'préstamo'
        verbose_name_plural = 'préstamos'
        ordering = ['-fecha_solicitud', '-id']

    def __str__(self):
        return f'{self.herramienta} → {self.socio.username} ({self.get_estado_display()})'
