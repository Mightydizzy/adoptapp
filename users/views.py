from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from pets.models import Reaccion
from .forms import CustomUserCreationForm, CustomAuthenticationForm, EditarPerfilForm, CambiarPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # iniciar sesión automáticamente después de registrarse
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")  # en realidad es el email
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = CustomAuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home_view(request):
    return render(request, "home.html")

@login_required
def perfil_usuario(request):
    user = request.user
    likes = Reaccion.objects.filter(usuario=user, accion="like").select_related("mascota")
    return render(request, "users/perfil.html", {"usuario": user, "likes": likes})

@login_required
def editar_perfil(request):
    if request.method == "POST":
        form = EditarPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente ✅")
            return redirect("perfil")
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, "users/editar_perfil.html", {"form": form})

@login_required
def cambiar_password(request):
    if request.method == "POST":
        form = CambiarPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Contraseña cambiada correctamente 🔒")
            return redirect("perfil")
    else:
        form = CambiarPasswordForm(user=request.user)
    return render(request, "users/cambiar_password.html", {"form": form})