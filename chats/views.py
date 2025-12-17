from django.db import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, Message
from django.db.models import Q
from django.shortcuts import get_object_or_404



@login_required
def chat_list(request):
    quiero_adoptar = Conversation.objects.filter(adoptante=request.user)
    interesados = Conversation.objects.filter(publicador=request.user)

    return render(request, "chats/chats.html", {
        "quiero_adoptar": quiero_adoptar,
        "interesados": interesados,
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Conversation, Message
from pets.models import Mascota


@login_required
def mis_chats(request):
    # Conversaciones donde soy adoptante o publicador
    convs = (Conversation.objects
             .filter(Q(adoptante=request.user) | Q(publicador=request.user))
             .select_related("mascota", "adoptante", "publicador")
             .order_by("-created_at"))

    # Separación UX:
    # - "Me interesan": yo soy adoptante
    # - "Interesados": yo soy publicador
    me_interesan = [c for c in convs if c.adoptante_id == request.user.id]
    interesados = [c for c in convs if c.publicador_id == request.user.id]

    return render(request, "chats/mis_chats.html", {
        "me_interesan": me_interesan,
        "interesados": interesados,
    })


@login_required
def chats_por_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Solo el publicador puede ver los chats de ESA mascota
    if mascota.publicador_id != request.user.id:
        return redirect("mis_chats")

    convs = (Conversation.objects
             .filter(mascota=mascota)
             .select_related("adoptante", "publicador", "mascota")
             .order_by("-created_at"))

    return render(request, "chats/chats_por_mascota.html", {
        "mascota": mascota,
        "convs": convs,
    })


@login_required
def chat_detalle(request, chat_id):
    convo = get_object_or_404(
        Conversation.objects.select_related("mascota", "adoptante", "publicador"),
        id=chat_id
    )

    if request.user.id not in (convo.adoptante_id, convo.publicador_id):
        return redirect("mis_chats")

    Message.objects.filter(conversation=convo).exclude(sender=request.user).update(is_read=True)

    if request.method == "POST":
        text = (request.POST.get("text") or "").strip()
        if text:
            Message.objects.create(conversation=convo, sender=request.user, text=text)
        return redirect(request.path)


    mensajes = (Message.objects
                .filter(conversation=convo)
                .select_related("sender")
                .order_by("created_at"))

    # Para el encabezado tipo "X está interesado en Y"
    interesado = convo.adoptante  # el que dio like / adoptante
    return render(request, "chats/chat_detalle.html", {
        "convo": convo,
        "mensajes": mensajes,
        "interesado": interesado,
    })


@login_required
def chats_por_mascota(request, mascota_id):
    chats = Conversation.objects.filter(
        mascota_id=mascota_id,
        publicador=request.user
    ).select_related("adoptante", "mascota")

    return render(request, "chats/chats_por_mascota.html", {
        "chats": chats
    })

