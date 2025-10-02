from django import forms
from .models import Mascota

class MascotaForm(forms.ModelForm):
    # Campos de edad separados (años + meses)
    edad_anios = forms.IntegerField(
        min_value=0,
        required=False,
        label="Años",
        error_messages={
            "min_value": "El número de años no puede ser negativo.",
            "invalid": "Ingresa un número válido de años."
        },
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    edad_meses_extra = forms.IntegerField(
        min_value=0,
        max_value=11,
        required=False,
        label="Meses",
        error_messages={
            "min_value": "El número de meses no puede ser negativo.",
            "max_value": "El número de meses debe ser 11 o menos.",
            "invalid": "Ingresa un número válido de meses."
        },
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Mascota
        fields = ["nombre", "especie", "tamaño", "ciudad", "foto", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "especie": forms.Select(attrs={"class": "form-select"}),
            "tamaño": forms.Select(attrs={"class": "form-select"}),
            "ciudad": forms.TextInput(attrs={"class": "form-control"}),
            "foto": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def save(self, commit=True, publicador=None):
        mascota = super().save(commit=False)
        # Convertir años y meses a meses totales
        anios = self.cleaned_data.get("edad_anios") or 0
        meses = self.cleaned_data.get("edad_meses_extra") or 0
        mascota.edad_meses = anios * 12 + meses

        if publicador:
            mascota.publicador = publicador
        if commit:
            mascota.save()
        return mascota