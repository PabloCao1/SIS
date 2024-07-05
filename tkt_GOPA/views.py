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
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .forms import *
from .models import *

class TicketGOPACreateView(CreateView):
    model = TicketGOPA
    form_class = TicketGOPAFORM
    success_url = reverse_lazy('tktGOPA_list') 
    success_message = "Registro creado correctamente"

    def form_valid(self, form):
        # Asignar el valor al campo ticket antes de guardar el formulario
        year = timezone.now().year
        ticket_id = TicketGOPA.objects.latest('id').id + 1 if TicketGOPA.objects.exists() else 1  # Obtener el siguiente ID disponible
        ticket_value = f"TK-{year}-{ticket_id}"
        form.instance.ticket = ticket_value

        response = super().form_valid(form)
        
        # Procesar los turnos generados
        ticket = form.instance
        turnos = []
        i = 0
        while True:
            cantidad_turnos_key = f"cantidad_turnos_{i}"
            hora_turno_key = f"hora_turno_{i}"
            if cantidad_turnos_key not in self.request.POST or hora_turno_key not in self.request.POST:
                break
            cantidad_turnos = self.request.POST.get(cantidad_turnos_key)
            hora_turno = self.request.POST.get(hora_turno_key)
            turnos.append(TurnosHorarios(fk_ticket=ticket, hora=hora_turno, cantidad=cantidad_turnos))
            i += 1

        # Guardar los turnos
        TurnosHorarios.objects.bulk_create(turnos)

        return response

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        #print(form.errors)
        return self.render_to_response(context)

class TicketGOPAUpdateView(SuccessMessageMixin, UpdateView):
    # permission_required = ""
    model = TicketGOPA
    form_class = TicketGOPAFORM
    success_url = reverse_lazy('tktGOPA_list') 
    success_message = "Registro actualizado correctamente"

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('tktGOPA_detail', args=(self.object.pk,)))

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        #print(form.errors)
        return self.render_to_response(context)

class TicketGOPAListView(ListView):
    #permission_required = ""
    model = TicketGOPA

class TicketGOPADetailView(DetailView):
    #permission_required = ""
    model = TicketGOPA

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turnos'] = TurnosHorarios.objects.filter(fk_ticket=self.object)
        return context

    def post(self, request, *args, **kwargs):
        # Obtener el objeto TicketGOPA
        ticket_gopa = self.get_object()

        # Obtener el nuevo estado del formulario
        nuevo_estado = request.POST.get('estado')

        # Actualizar el estado del TicketGOPA
        ticket_gopa.estado = nuevo_estado
        ticket_gopa.save()

        # Redireccionar a alguna página después de guardar el estado
        return HttpResponseRedirect(reverse('tktGOPA_detail', args=(ticket_gopa.pk,)))

class TicketGOPADeleteView(DeleteView):
    #permission_required = ""
    model = TicketGOPA
    success_url = reverse_lazy('tktGOPA_list') 