from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    View,
    FormView,
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, Count, Case, When
from datetime import date
from itertools import chain

from .forms import *
from .models import *
from sedes.models import Sedes

# region ------------------------------------------------------------------------- EMPLEADOS


class EmpleadoListView(PermissionRequiredMixin, ListView):
    permission_required = "rrhh.view_empleado"
    model = Empleado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sedes_queryset = Sedes.objects.all() 
        # Crea una lista de tuplas (id, nombre) para las opciones del select
        opciones_sedes = [(sede.id, sede.nombre) for sede in sedes_queryset]
        context['opciones_sedes'] = opciones_sedes

        return context

    #  devuelve queryset completo o filtrado segun busqueda
    def get_queryset(self):
        palabra = self.request.GET.get("busqueda", None)
        object_list = self.model.objects.all()

        if palabra:
            object_list = object_list.filter(
                Q(apellido__icontains=palabra) | Q(dni=palabra)
            )

        object_list = object_list.distinct()
        return object_list


class EmpleadoCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "rrhh.add_empleado"
    model = Empleado
    form_class = EmpleadoForm
    success_message = "Registro creado correctamente"


class EmpleadoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "rrhh.change_empleado"
    model = Empleado
    form_class = EmpleadoForm
    success_message = "Registro actualizado correctamente"


class EmpleadoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "rrhh.view_empleado"
    model = Empleado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = self.get_object()

        # region-----INICIO PROCESAMIENTO EVENTOS-----------------------------------------<<
        eventos = EmpleadoEvento.objects.filter(empleado=empleado)
        cant_eventos_asistio= 0
        porcentaje_eventos_asistio = 0
        if eventos:
            cant_eventos_asistio = eventos.filter(asistio=True).count()
            porcentaje_eventos_asistio = int(
                cant_eventos_asistio * 100 / eventos.count()
            )
        eventos_empleado = eventos[:5]
        # endregion-----FIN PROCESAMIENTO EVENTOS-----------------------------------------<<

        # region---INICIO PROCESAMIENTO LICENCIAS-----------------------------------------<<

        licencias_ordinarias = EmpleadoLicencia.objects.filter(
            fk_empleado=empleado.id, tipo="ORDINARIA"
        )
        licencias_especiales = EmpleadoLicencia.objects.filter(
            fk_empleado=empleado.id, tipo="ESPECIAL"
        )

        total_ordinarias = 0
        if licencias_ordinarias:  # Cálculo de dias disponibles de licencia ordinaria
            licencias_actuales = licencias_ordinarias.filter(
                fecha_desde__year__gte=date.today().year
            )  # toma solo las del año en evento
            for l in licencias_actuales:
                total_ordinarias += l.dias_tomados()

        total_especiales = 0
        if licencias_especiales:
            for (
                l
            ) in (
                licencias_especiales
            ):  # Cálculo de total de días tomados por licencias especiales
                total_especiales += l.dias_tomados()

        if (
            empleado.vacaciones_anuales
        ):  # Cálculo de total de ddisponibles por licencias ordinarias
            vacaciones_disponibles = (
                str(empleado.vacaciones_anuales - total_ordinarias)
                + "/"
                + str(empleado.vacaciones_anuales)
            )
        else:
            vacaciones_disponibles = ": no registrado"

        # Combinar licencias y traspasos en un solo queryset para mostrarlos en la timeline
        # Obtener instancias de EmpleadoLicencia y EmpleadoTraspaso
        licencias = EmpleadoLicencia.objects.filter(fk_empleado=empleado.id)
        traspasos = EmpleadoTraspaso.objects.filter(fk_empleado=empleado.id)
        timeline_historial = list(chain(licencias, traspasos))
        # endregion FIN PROCESAMIENTO LICENCIAS------------------------------------------------------

        context["total_especiales"] = total_especiales
        context["licencias_ordinarias"] = licencias_ordinarias
        context["licencias_especiales"] = licencias_especiales
        context["vacaciones_disponibles"] = vacaciones_disponibles
        context["form_agregar_traspaso"] = EmpleadoTraspasosForm(instance=self.object)
        context["form_agregar_evento"] = EmpleadoEventoForm(instance=self.object)
        context["form_agregar_licencia"] = EmpleadoLicenciaForm(instance=self.object)
        context["timeline_historial"] = timeline_historial
        context["cant_eventos"] = eventos.count()
        context["eventos_empleado"] = eventos_empleado
        context["cant_eventos_asistio"] = cant_eventos_asistio
        context["porcentaje_eventos_asistio"] = porcentaje_eventos_asistio
        return context


class EmpleadoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "rrhh.delete_empleado"
    model = Empleado
    success_url = reverse_lazy("empleado_list")
    success_message = "Registro eliminado correctamente"


class EmpleadoCambiarEstadoView(PermissionRequiredMixin, View):
    permission_required = "rrhh.change_empleado"

    def post(self, request, *args, **kwargs):
        # Obtener el objeto de tu modelo
        id = request.POST.get("id")
        objeto = Empleado.objects.get(pk=id)
        # Cambiar el estado booleano
        objeto.activo = not objeto.activo
        objeto.save()
        if not objeto.activo:
            objeto.fecha_baja = datetime.datetime.now()
            objeto.save()
        else:
            objeto.fecha_baja = None
            objeto.save()
        return JsonResponse({"status": "success"})


class EmpleadoTraspasosFormView(PermissionRequiredMixin, FormView):
    permission_required = "rrhh.add_empleadotraspaso"
    form_class = EmpleadoTraspasosForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        errors = dict(form.errors)
        return JsonResponse({"success": False, "errors": errors}, status=400)


class EmpleadoLicenciasFormView(PermissionRequiredMixin, FormView):
    permission_required = "rrhh.add_empleadolicencia"
    form_class = EmpleadoLicenciaForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        errors = dict(form.errors)
        return JsonResponse({"success": False, "errors": errors}, status=400)


class EmpleadoLicenciasDelete(PermissionRequiredMixin, View):
    permission_required = "rrhh.delete_empleadolicencia"

    def post(self, request, *args, **kwargs):
        empleado_id = request.POST.get("empleadoID")
        licencia_id = request.POST.get("licenciaID")

        licencia = EmpleadoLicencia.objects.get(id=licencia_id, fk_empleado=empleado_id)

        if licencia:
            licencia.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": errors}, status=400)


# endregion


# region ------------------------------------------------------------------------- EVENTOS
class EventoListView(PermissionRequiredMixin, ListView):
    permission_required = "rrhh.view_evento"
    model = Evento

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            total_inscritos=Count("empleadoevento"),
            total_asistio=Count(
                Case(
                    When(empleadoevento__asistio=True, then=1),
                    output_field=models.IntegerField(),
                )
            ),
        )
        return queryset


class EventoCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "rrhh.add_evento"
    model = Evento
    form_class = EventoForm
    success_message = "Registro creado correctamente"


class EventoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "rrhh.update_evento"
    model = Evento
    form_class = EventoForm
    success_message = "Registro actualizado correctamente"


class EventoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "rrhh.view_evento"
    model = Evento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()

        total_inscritos = EmpleadoEvento.objects.filter(evento=evento).count()
        total_asistio = EmpleadoEvento.objects.filter(evento=evento, asistio=True).count()

        context["total_inscritos"] = total_inscritos
        context["total_asistio"] = total_asistio

        return context


class EventoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "rrhh.delete_evento"
    model = Evento
    success_url = reverse_lazy("evento_list")
    success_message = "Registro eliminado correctamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()

        # Crear una lista para almacenar los nombres de las relaciones existentes
        relaciones_existentes = []

        # Agregar los nombres de las relaciones existentes a la lista
        if EmpleadoEvento.objects.filter(evento=evento).exists():
            relaciones_existentes.append("Empleados")

        # Agregar la lista de nombres de relaciones al contexto
        context["relaciones_existentes"] = relaciones_existentes
        return context


# endregion

# region ------------------------------------------------------------ EVENTOS DEL EMPLEADO -
class EmpleadoEventoListView(PermissionRequiredMixin, ListView):
    permission_required = "rrhh.view_empleadoevento"
    model = EmpleadoEvento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs["emp_id"]
        # empleado = Empleado.objects.get(id=id)
        empleado = Empleado.objects.values('nombres', 'apellidos', 'CUIT', 'sede', "id").get(id=id)
        context["form_agregar_evento"] = EmpleadoEventoForm()
        context['empleado'] = empleado

        return context

    #  devuelve queryset completo o filtrado segun busqueda
    def get_queryset(self):
        palabra = self.request.GET.get("busqueda", None)
        id = self.kwargs["emp_id"]
        object_list = self.model.objects.filter(empleado__id=id).order_by('-evento__fecha')

        if palabra:
            object_list = object_list.filter(
                Q(evento__nombre__icontains=palabra) | Q(evento__modalidad=palabra) | Q(evento__fk_tipo__nombre = palabra)
            )

        object_list = object_list.distinct()
        return object_list
    

class EmpleadoEventosDeleteAjax(PermissionRequiredMixin, View):
    permission_required = "rrhh.delete_empleadoevento"

    def post(self, request, *args, **kwargs):
        empleado_id = request.POST.get("empleadoID")
        evento_id = request.POST.get("eventoID")

        evento = EmpleadoEvento.objects.get(id=evento_id, empleado__id=empleado_id)

        if evento:
            evento.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": errors}, status=400)


class EmpleadoEventoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "rrhh.delete_empleadoevento"
    model = EmpleadoEvento
    success_url = reverse_lazy("empleado_list")
    success_message = "Registro eliminado correctamente"


class EmpleadoAgregarEventoFormView(PermissionRequiredMixin, FormView):
    permission_required = "rrhh.add_empleadoevento"
    form_class = EmpleadoEventoForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        errors = dict(form.errors)
        return JsonResponse({"success": False, "errors": errors}, status=400)


class ActualizarAsistioView(PermissionRequiredMixin,View):
    permission_required = "rrhh.update_empleadoevento"

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            empleado_evento_id = request.POST.get('id')
            asistio = request.POST.get('asistio')
            
            try:
                empleado_evento = EmpleadoEvento.objects.get(pk=empleado_evento_id)
                empleado_evento.asistio = asistio
                empleado_evento.save()
                
                return JsonResponse({'success': True})
            except EmpleadoEvento.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'No existe el Evento asociado al Empleado.'})
        else:
            return JsonResponse({'success': False, 'error': 'Petición inválida'})

# endregion