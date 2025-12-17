from django.urls import path
from . import views

urlpatterns = [
    path("publicar/", views.publicar_mascota, name="publicar"),
    path("descubrir/", views.descubrir_mascotas, name="descubrir"),
    path("reaccionar/<int:mascota_id>/", views.reaccionar_mascota, name="reaccionar_mascota"),
    path("segunda-oportunidad/", views.segunda_oportunidad, name="segunda_oportunidad"),
    path("mis-mascotas/", views.mis_mascotas, name="mis_mascotas"),
    path("editar/<int:mascota_id>/", views.editar_mascota, name="editar_mascota"),
    path("estado/<int:mascota_id>/", views.cambiar_estado_mascota, name="cambiar_estado_mascota"),
    path("notificaciones/", views.notificaciones, name="notificaciones"),
    path("notificaciones/abrir/<int:notif_id>/", views.abrir_notificacion_like, name="abrir_notificacion_like"),
    path("api/regiones/", views.api_regiones, name="api_regiones"),
    path("api/regiones/<str:region_id>/comunas/", views.api_comunas, name="api_comunas"),
]
