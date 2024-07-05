from django.urls import path
from .views import *

urlpatterns = [
    path("empleado/listar", EmpleadoListView.as_view(), name="empleado_list"),
    path("empleado/agregar", EmpleadoCreateView.as_view(), name="empleado_add"),
    path("empleado/ver/<pk>", EmpleadoDetailView.as_view(), name="empleado_detail"),
    path(
        "empleado/modificar/<pk>", EmpleadoUpdateView.as_view(), name="empleado_change"
    ),
    path(
        "empleado/eliminar/<pk>", EmpleadoDeleteView.as_view(), name="empleado_delete"
    ),
    path(
        "empleado/cambiar_estado/",
        EmpleadoCambiarEstadoView.as_view(),
        name="empleado-activar-desactivar",
    ),
    path(
        "empleado/traspasos/",
        EmpleadoTraspasosFormView.as_view(),
        name="empleado-traspasos",
    ),
    path(
        "empleado/licencias/agregar/",
        EmpleadoLicenciasFormView.as_view(),
        name="empleado-agregar-licencias",
    ),
    path(
        "empleado/licencias/borrar/",
        EmpleadoLicenciasDelete.as_view(),
        name="empleado-borrar-licencias",
    ),
    path(
        "empleado/eventos/borrar/",
        EmpleadoEventosDeleteAjax.as_view(),
        name="empleado-borrar-eventos",
    ),
    path(
        "empleado/eventos/borrar/<pk>",
        EmpleadoEventoDeleteView.as_view(),
        name="empleado-borrar-evento",
    ),
    path(
        "empleado/eventos/agregar/",
        EmpleadoAgregarEventoFormView.as_view(),
        name="empleado-agregar-evento",
    ),
    
    # EVENTOS DEL EMPLEADO
    path("empleado/listaeventos/<emp_id>", EmpleadoEventoListView.as_view(), name="empleadoevento_list"),
    path('actualizar-asistio/', ActualizarAsistioView.as_view(), name='actualizar_asistio'),
    # EVENTOS
    path("eventos/", EventoListView.as_view(), name="evento_list"),
    path("eventos/crear/", EventoCreateView.as_view(), name="evento_create"),
    path("eventos/editar/<int:pk>/", EventoUpdateView.as_view(), name="evento_update"),
    path("eventos/ver/<int:pk>/", EventoDetailView.as_view(), name="evento_detail"),
    path("eventos/eliminar/<int:pk>/", EventoDeleteView.as_view(), name="evento_delete"),

]
