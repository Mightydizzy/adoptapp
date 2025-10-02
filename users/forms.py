from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, PasswordChangeForm
from .models import CustomUser, validar_rut
import re


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("rut", "username", "email", "first_name", "last_name")

    # Validación de RUT usando tu función
    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        validar_rut(rut)  # lanza ValidationError si no es válido
        return rut

    # Validación para nombres → solo letras y espacios
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', first_name):
            raise forms.ValidationError("El nombre solo puede contener letras.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            raise forms.ValidationError("El apellido solo puede contener letras.")
        return last_name

    # Confirmar contraseñas
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "ciudad", "foto_perfil"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "ciudad": forms.TextInput(attrs={"class": "form-control"}),
            "foto_perfil": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class CambiarPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
