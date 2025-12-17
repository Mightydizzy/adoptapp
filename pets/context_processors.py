from .models import Notificacion

def notificaciones_dropdown(request):
    if request.user.is_authenticated:
        items = (Notificacion.objects
                 .filter(destinatario=request.user, leida=False)
                 .select_related("actor", "mascota")
                 .order_by("-created_at")[:5])
        count = Notificacion.objects.filter(destinatario=request.user, leida=False).count()
        return {"notif_items": items, "notif_count": count}
    return {"notif_items": [], "notif_count": 0}
