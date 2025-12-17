from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MascotaForm
from .models import Mascota, Reaccion, Notificacion
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from chats.models import Conversation
from .services.dpa_local import load_data


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
    Mascota.objects.filter(disponible=True)
    vistas = Reaccion.objects.filter(usuario=request.user).values_list("mascota_id", flat=True)

    mascotas = Mascota.objects.exclude(publicador=request.user).exclude(id__in=vistas).order_by("-fecha_publicacion")

    return render(request, "pets/descubrir.html", {"mascotas": mascotas})


@login_required
def reaccionar_mascota(request, mascota_id):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=400)

    accion = request.POST.get("accion")
    mascota = get_object_or_404(Mascota, id=mascota_id)

    prev = Reaccion.objects.filter(usuario=request.user, mascota=mascota).first()

    Reaccion.objects.update_or_create(
        usuario=request.user,
        mascota=mascota,
        defaults={"accion": accion}
    )

    like_nuevo = (accion == "like" and (prev is None or prev.accion != "like"))

    if like_nuevo and mascota.publicador != request.user:
        Notificacion.objects.create(
            destinatario=mascota.publicador,
            actor=request.user,
            mascota=mascota,
            tipo="like",
            mensaje=f"¡A {request.user.username} le ha gustado {mascota.nombre}! Haz click aquí para enviarle un mensaje."
        )

        from chats.models import Conversation
        Conversation.objects.get_or_create(
            mascota=mascota,
            adoptante=request.user,
            defaults={"publicador": mascota.publicador}
        )

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"success": True, "accion": accion})
    return redirect("segunda_oportunidad")

@login_required
def segunda_oportunidad(request):
    reacciones = Reaccion.objects.filter(usuario=request.user, accion="descartar").select_related("mascota")
    return render(request, "pets/segunda_oportunidad.html", {"reacciones": reacciones})

@login_required
def mis_mascotas(request):
    mascotas = Mascota.objects.filter(publicador=request.user).order_by("-id")
    return render(request, "pets/mis_mascotas.html", {"mascotas": mascotas})

@login_required
def cambiar_estado_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id, publicador=request.user)

    if request.method != "POST":
        return redirect("mis_mascotas")

    password = request.POST.get("password", "")
    nuevo_estado = request.POST.get("disponible")  # "1" o'state'

    user = authenticate(request, username=request.user.username, password=password)
    if user is None:
        messages.error(request, "Contraseña incorrecta. No se cambió el estado.")
        return redirect("mis_mascotas")

    mascota.disponible = (nuevo_estado == "1")
    mascota.save(update_fields=["disponible"])

    if mascota.disponible:
        messages.success(request, f"{mascota.nombre} volvió a estar Disponible.")
    else:
        messages.success(request, f"{mascota.nombre} quedó como No disponible.")

    return redirect("mis_mascotas")


@login_required
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id, publicador=request.user)

    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, "Mascota actualizada.")
            return redirect("mis_mascotas")
    else:
        form = MascotaForm(instance=mascota)

    return render(request, "pets/editar_mascota.html", {"form": form, "mascota": mascota})

@login_required
def notificaciones(request):
    items = Notificacion.objects.filter(destinatario=request.user).select_related("actor", "mascota").order_by("-created_at")
    return render(request, "pets/notificaciones.html", {"items": items})



@login_required
def abrir_notificacion_like(request, notif_id):
    notif = get_object_or_404(Notificacion, id=notif_id, destinatario=request.user)


    notif.leida = True
    notif.save(update_fields=["leida"])

    mascota = notif.mascota
    actor = notif.actor
    publicador = mascota.publicador

    convo, _ = Conversation.objects.get_or_create(
        mascota=mascota,
        adoptante=actor,
        defaults={"publicador": publicador}
    )

    return redirect("chat_detalle", convo.id)



@login_required
def api_regiones(request):
    data = load_data()
    payload = [{"id": r["id"], "nombre": r["region"]} for r in data["regiones"]]
    return JsonResponse(payload, safe=False)

@login_required
def api_comunas(request, region_id):
    data = load_data()
    region = next((r for r in data["regiones"] if r["id"] == region_id), None)
    if not region:
        return JsonResponse({"error": "Región no encontrada"}, status=404)
    return JsonResponse([{"nombre": c} for c in region["comunas"]], safe=False)
