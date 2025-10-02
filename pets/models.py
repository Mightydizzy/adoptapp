from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class Mascota(models.Model):
    SPECIES = [
        ("perro", "Perro"),
        ("gato", "Gato"),
        ("otro", "Otro"),
    ]

    SIZES = [
        ("pequeño", "Pequeño"),
        ("mediano", "Mediano"),
        ("grande", "Grande"),
    ]
    SEXO_CHOICES = [
        ("M", "Macho"),
        ("H", "Hembra"),
    ]

    nombre = models.CharField(max_length=50)
    especie = models.CharField(max_length=20, choices=SPECIES)
    edad_meses = models.PositiveIntegerField(default=0)
    tamaño = models.CharField(max_length=20, choices=SIZES)
    ciudad = models.CharField(max_length=50)
    foto = CloudinaryField("Foto de la mascota")
    descripcion = models.TextField(blank=True)


    def edad_legible(self):
        if self.edad_meses < 12:
            return f"{self.edad_meses} mes(es)"
        else:
            anios = self.edad_meses // 12
            meses = self.edad_meses % 12
            if meses:
                return f"{anios} año(s) {meses} mes(es)"
            return f"{anios} año(s)"

    publicador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mascotas")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.especie})"

class Reaccion(models.Model):
    ACCIONES = [
        ("like", "Like"),
        ("descartar", "Descartar"),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mascota = models.ForeignKey("pets.Mascota", on_delete=models.CASCADE)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "mascota")  # un usuario no puede reaccionar 2 veces a la misma mascota
