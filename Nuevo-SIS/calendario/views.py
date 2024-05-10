from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from rrhh.models import Empleado
import json
from datetime import datetime


class CalendarioTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "calendario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Empleado.objects.exclude(fecha_nacimiento__isnull=True)
        cumpleanos_data = []
        for empleado in queryset:

            empleado_dict = {
                "title": f" {empleado.apellidos} {empleado.nombres}",
                "start": empleado.fecha_nacimiento.replace(
                    year=datetime.now().year
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "url": reverse("empleado_detail", kwargs={"pk": empleado.id}),
                "allDay": "true",
                "extendedProps": {
                    "fechaNacimiento": empleado.fecha_nacimiento.strftime("%d/%m/%Y"),
                    "edad": empleado.edad(),
                    "GO_equipo": empleado.GO_equipo or "-",
                    "sede": empleado.sede or "-",
                },
                "tipo": "cumpleanos",
                "cid": "1",
                "className": ["cumple", "bg-gradient-cyan text-white"],
                "borderColor": "#0dcaf0",
            }
            cumpleanos_data.append(empleado_dict)
        cumpleanos_json = json.dumps(cumpleanos_data)
        context["cumpleanos_json"] = cumpleanos_json
        return context
