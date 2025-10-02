from django.urls import path
from . import views

urlpatterns = [
    path("publicar/", views.publicar_mascota, name="publicar"),
    path("descubrir/", views.descubrir_mascotas, name="descubrir"),
    path("reaccionar/<int:mascota_id>/", views.reaccionar_mascota, name="reaccionar_mascota"),
    path("segunda-oportunidad/", views.segunda_oportunidad, name="segunda_oportunidad"),
]
