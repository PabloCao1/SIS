from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView,
)
from .models import *
from .forms import *
from django.db.models import Q, Count
from django.db import transaction
import datetime

# Sedes


class SedesListView(ListView):
    # permission_required = ['Usuarios.rol_admin','Usuarios.rol_observador','Usuarios.rol_consultante']
    model = Sedes

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query) | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class SedesDetailView(DetailView):
    # permission_required = ['Usuarios.rol_admin','Usuarios.rol_observador','Usuarios.rol_consultante']
    model = Sedes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        sede = self.get_object()  # Obtener la instancia de Sedes

        # Obtener todos los trámites relacionados con la sede
        tramites = sede.tramites.all()
        imagenes = SedesArchivos.objects.filter(fk_sedes=pk).all()
        planos = SedesPlanos.objects.filter(fk_sedes=pk).all()

        # Crear un diccionario para almacenar los trámites agrupados por servicio
        tramites_por_servicio = {}

        # Organizar los trámites por servicio
        for tramite in tramites:
            nombre_servicio = tramite.fk_servicio.nombre
            nombre_tramite = tramite.nombre

            if nombre_servicio not in tramites_por_servicio:
                tramites_por_servicio[nombre_servicio] = []

            tramites_por_servicio[nombre_servicio].append(nombre_tramite)

        context["tramites_por_servicio"] = (
            tramites_por_servicio  # Agregar los trámites por servicio al contexto
        )
        context["tramites"] = tramites
        context["count_tramites"] = tramites.count()
        context["count_turno"] = tramites.filter(turnos=True).count()
        context["count_espontaneo"] = tramites.filter(espontaneos=True).count()
        context["imagenes"] = imagenes
        context["planos"] = planos

        return context


class SedesCreateView(SuccessMessageMixin, CreateView):
    # permission_required = 'Usuarios.rol_admin'
    model = Sedes
    form_class = SedesForm
    success_message = "%(nombre)s fue registrado correctamente"

    def form_valid(self, form):
        archivos = self.request.FILES.getlist("archivos")
        planos = self.request.FILES.getlist("planos")
        with transaction.atomic():
            self.object = form.save()

            # Crear instancias de SedesArchivos
            if archivos:
                for archivo in archivos:
                    SedesArchivos.objects.create(
                        fk_sedes=self.object, archivo=archivo, tipo="imagen"
                    )

            # Crear instancias de SedesPlanos
            if planos:
                for plano in planos:
                    SedesPlanos.objects.create(
                        fk_sedes=self.object, planos=plano, tipo="imagen"
                    )

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class SedesUpdateView(SuccessMessageMixin, UpdateView):
    # permission_required = 'Usuarios.rol_admin'
    model = Sedes
    form_class = SedesForm
    success_message = "%(nombre)s fue editado correctamente"

    def form_valid(self, form):
        archivos = self.request.FILES.getlist("archivos")
        planos = self.request.FILES.getlist("planos")
        images_to_delete = self.request.POST.get("images_to_delete", "")
        planos_to_delete = self.request.POST.get("planos_to_delete", "")

        if images_to_delete:
            images_to_delete_ids = images_to_delete.split(",")
            SedesArchivos.objects.filter(id__in=images_to_delete_ids).delete()

        if planos_to_delete:
            planos_to_delete_ids = planos_to_delete.split(",")
            SedesPlanos.objects.filter(id__in=planos_to_delete_ids).delete()

        if archivos:
            for archivo in archivos:
                SedesArchivos.objects.create(
                    fk_sedes=form.instance, archivo=archivo, tipo="imagen"
                )

        if planos:
            for plano in planos:
                SedesPlanos.objects.create(
                    fk_sedes=form.instance, planos=plano, tipo="plano"
                )

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["imagenes"] = SedesArchivos.objects.filter(
            fk_sedes=self.object, tipo="imagen"
        )
        context["planos"] = SedesPlanos.objects.filter(
            fk_sedes=self.object, tipo="plano"
        )
        return context


class SedesDeleteView(SuccessMessageMixin, DeleteView):
    # permission_required = 'Usuarios.rol_admin'
    model = Sedes
    success_url = reverse_lazy("listar_sede")
    success_message = "El registro fue eliminado correctamente"


# Servicios


class ServiciosListView(ListView):
    # permission_required = ['Usuarios.rol_admin','Usuarios.rol_observador','Usuarios.rol_consultante']
    model = Servicios

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query) | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class ServiciosDetailView(DetailView):
    # permission_required = ['Usuarios.rol_admin','Usuarios.rol_observador','Usuarios.rol_consultante']
    model = Servicios


class ServiciosCreateView(SuccessMessageMixin, CreateView):
    # permission_required = 'Usuarios.rol_admin'
    model = Servicios
    form_class = ServiciosForm
    success_message = "%(nombre)s fue registrado correctamente"


class ServiciosDeleteView(SuccessMessageMixin, DeleteView):
    # permission_required = 'Usuarios.rol_admin'
    model = Servicios
    success_url = reverse_lazy("listar_servicios")
    success_message = "El registro fue eliminado correctamente"


class ServiciosUpdateView(SuccessMessageMixin, UpdateView):
    # permission_required = 'Usuarios.rol_admin'
    model = Servicios
    form_class = ServiciosForm
    success_message = "%(nombre)s fue editado correctamente"


# Tramites


class TramitesListView(ListView):
    # permission_required = ['Usuarios.rol_admin','Usuarios.rol_observador','Usuarios.rol_consultante']
    model = Tramites

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query) | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class TramitesDetailView(DetailView):
    # permission_required = ['Usuarios.rol_admin','Usuarios.rol_observador','Usuarios.rol_consultante']
    model = Tramites


class TramitesCreateView(SuccessMessageMixin, CreateView):
    # permission_required = 'Usuarios.rol_admin'
    model = Tramites
    form_class = TramitesForm
    success_message = "%(nombre)s fue registrado correctamente"


class TramitesDeleteView(SuccessMessageMixin, DeleteView):
    # permission_required = 'Usuarios.rol_admin'
    model = Tramites
    success_url = reverse_lazy("listar_tramites")
    success_message = "El registro fue eliminado correctamente"


class TramitesUpdateView(SuccessMessageMixin, UpdateView):
    # permission_required = 'Usuarios.rol_admin'
    model = Tramites
    form_class = TramitesForm
    success_message = "%(nombre)s fue editado correctamente"
