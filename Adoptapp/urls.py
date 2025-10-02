from django.contrib import admin
from django.urls import path, include
from pets import views
from django.conf import settings



urlpatterns = [
    path("", include("users.urls")),
    path("mascotas/", include("pets.urls")),
    path("", views.descubrir_mascotas, name="home"),
    
]

if settings.DEBUG:
    urlpatterns += [path("admin/", admin.site.urls)]

