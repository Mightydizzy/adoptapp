from django.contrib import admin
from django.urls import path, include
from pets import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("mascotas/", include("pets.urls")),
    path("", views.descubrir_mascotas, name="home"),
]


