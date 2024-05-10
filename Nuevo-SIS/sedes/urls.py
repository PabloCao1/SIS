from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # Sede
    path("crear", SedesCreateView.as_view(), name="crear_sede"),
    path("listar", SedesListView.as_view(), name="listar_sede"),
    path("ver/<pk>", SedesDetailView.as_view(), name="ver_sede"),
    path("editar/<pk>", SedesUpdateView.as_view(), name="editar_sede"),
    path("eliminar/<pk>", SedesDeleteView.as_view(), name="eliminar_sede"),
    # Servicios
    path("servicios/crear", ServiciosCreateView.as_view(), name="crear_servicios"),
    path("servicios/listar", ServiciosListView.as_view(), name="listar_servicios"),
    path("servicios/ver/<pk>", ServiciosDetailView.as_view(), name="ver_servicios"),
    path(
        "servicios/editar/<pk>", ServiciosUpdateView.as_view(), name="editar_servicios"
    ),
    path(
        "servicios/eliminar/<pk>",
        ServiciosDeleteView.as_view(),
        name="eliminar_servicios",
    ),
    # Tramites
    path("tramites/crear", TramitesCreateView.as_view(), name="crear_tramites"),
    path("tramites/listar", TramitesListView.as_view(), name="listar_tramites"),
    path("tramites/ver/<pk>", TramitesDetailView.as_view(), name="ver_tramites"),
    path("tramites/editar/<pk>", TramitesUpdateView.as_view(), name="editar_tramites"),
    path(
        "tramites/eliminar/<pk>", TramitesDeleteView.as_view(), name="eliminar_tramites"
    ),
]
