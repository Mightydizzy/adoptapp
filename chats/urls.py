from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_list, name="chat_list"),
    path("mascota/<int:mascota_id>/", views.chats_por_mascota, name="chats_por_mascota"),
    path("<int:chat_id>/", views.chat_detalle, name="chat_detalle"),
]
