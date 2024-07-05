from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # path("", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path("logout", CustomLogoutView.as_view(), name="logout"),
    path("set_dark_mode/", login_required(set_dark_mode), name="set_dark_mode"),

    # Usuarios
    path('administracion/usuarios/crear', login_required(UsuariosCreateView.as_view()),name='usuarios_crear'), 
    path('administracion/usuarios/listar', login_required(UsuariosListView.as_view()),name='usuarios_listar'), 
    path('administracion/usuarios/ver/<pk>', login_required(UsuariosDetailView.as_view()),name='usuarios_ver'), 
    path('administracion/usuarios/editar/<pk>', login_required(UsuariosUpdateView.as_view()),name='usuarios_editar'), 
    path('administracion/usuarios/eliminar/<pk>', login_required(UsuariosDeleteView.as_view()),name='usuarios_eliminar'),
    path('set_dark_mode/', login_required(set_dark_mode), name='set_dark_mode'), 
    
    # Password
    path('administracion/password-reset/<pk>', login_required(UsuariosResetPassView.as_view()),name='password_reset'), 

    # Perfil: acciones que realiza el usuario logeado
    path('administracion/perfil/editar/<pk>', login_required(PerfilUpdateView.as_view()),name='perfil_editar'), 
    path('administracion/perfil/cambiar_password', login_required(PerfilChangePassView.as_view()) ,name='cambiar_password'),

    # Grupos de usuario
    path('administracion/grupos/crear', login_required(GruposCreateView.as_view()),name='grupos_crear'), 
    path('administracion/grupos/listar', login_required(GruposListView.as_view()),name='grupos_listar'), 
    path('administracion/grupos/ver/<pk>', login_required(GruposDetailView.as_view()),name='grupos_ver'), 
    path('administracion/grupos/editar/<pk>', login_required(GruposUpdateView.as_view()),name='grupos_editar'), 
    path('administracion/grupos/eliminar/<pk>', login_required(GruposDeleteView.as_view()),name='grupos_eliminar'), 
]
