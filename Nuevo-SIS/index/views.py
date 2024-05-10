from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rrhh.models import Empleado, Evento
from sedes.models import Sedes


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        cant_empleados_activos = Empleado.objects.filter(activo=True).count()
        cant_eventos = Evento.objects.all().count()
        cant_sedes = Sedes.objects.all().count()

        context = {
            "cant_empleados_activos": cant_empleados_activos,
            "cant_eventos": cant_eventos,
            "cant_sedes": cant_sedes,
        }

        return context
