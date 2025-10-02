from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField   

def validar_rut(rut: str):
    rut = rut.upper().replace(".", "").replace("-", "")
    cuerpo, dv = rut[:-1], rut[-1]

    if not cuerpo.isdigit():
        raise ValidationError("El RUT debe tener números válidos.")

    suma = 0
    multiplicador = 2
    for num in reversed(cuerpo):
        suma += int(num) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    resto = suma % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_calculado = "0"
    elif dv_calculado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_calculado)

    if dv != dv_calculado:
        raise ValidationError("RUT inválido.")


class CustomUserManager(BaseUserManager):
    def create_user(self, email, rut, username, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo es obligatorio")
        if not rut:
            raise ValueError("El RUT es obligatorio")
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            rut=rut,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, rut, username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")

        return self.create_user(email, rut, username, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    foto_perfil = CloudinaryField(
        "Foto de perfil",         # 👈 verbose_name (lo que verás en admin y forms)
        folder="perfiles",
        blank=True,
        null=True,
        help_text="Sube una foto de perfil (opcional)."
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["rut", "username", "first_name", "last_name"]

    def __str__(self):
        return self.username

