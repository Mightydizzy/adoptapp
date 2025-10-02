from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MascotaForm
from .models import Mascota, Reaccion
from django.http import JsonResponse

@login_required
def publicar_mascota(request):
    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(publicador=request.user)
            return redirect("home")
        else:
            print("❌ Errores en el formulario:", form.errors)
    else:
        form = MascotaForm()
    return render(request, "pets/publicar.html", {"form": form})


@login_required
def descubrir_mascotas(request):
    # mascotas que ya tienen una reacción del usuario
    vistas = Reaccion.objects.filter(usuario=request.user).values_list("mascota_id", flat=True)

    # excluimos esas mascotas del descubrimiento
    mascotas = Mascota.objects.exclude(publicador=request.user).exclude(id__in=vistas).order_by("-fecha_publicacion")

    return render(request, "pets/descubrir.html", {"mascotas": mascotas})

@login_required
def reaccionar_mascota(request, mascota_id):
    if request.method == "POST":
        accion = request.POST.get("accion")
        mascota = get_object_or_404(Mascota, id=mascota_id)

        Reaccion.objects.update_or_create(
            usuario=request.user,
            mascota=mascota,
            defaults={"accion": accion}
        )

        # Si la petición viene de un form HTML, redirige
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True, "accion": accion})
        else:
            return redirect("segunda_oportunidad")

    return JsonResponse({"success": False}, status=400)
@login_required
def segunda_oportunidad(request):
    reacciones = Reaccion.objects.filter(usuario=request.user, accion="descartar").select_related("mascota")
    return render(request, "pets/segunda_oportunidad.html", {"reacciones": reacciones})
