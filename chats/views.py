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


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(
        Conversation,
        id=chat_id,
        chat = get_object_or_404(
            Conversation.objects.filter(Q(adoptante=request.user) | Q(publicador=request.user)),
            id=chat_id)
        )

    mensajes = chat.mensajes.select_related("sender").order_by("created_at")

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            Message.objects.create(
                conversation=chat,
                sender=request.user,
                text=text
            )
        return redirect("chat_detail", chat_id=chat.id)

    return render(request, "chats/chat_detail.html", {
        "chat": chat,
        "mensajes": mensajes,
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

