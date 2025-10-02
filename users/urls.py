from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("accounts/login/", views.login_view), 
    path("logout/", views.logout_view, name="logout"),
    path("", views.home_view, name="home"),
    path("perfil/", views.perfil_usuario, name="perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
    path("perfil/password/", views.cambiar_password, name="cambiar_password")
]