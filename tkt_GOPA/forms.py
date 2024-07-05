from django import forms
from django.forms import ValidationError
from .validators import *
from .models import *
from .choices import *

class TicketGOPAFORM(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

    class Meta:
        model = TicketGOPA
        fields = "__all__"
        widgets = {
            "fecha_publicacion": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "fecha_primer_turno": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            #"duracion_tramite": forms.NumberInput(attrs={"placeholder": "En minutos"}),
            #"dias_atencion": forms.SelectMultiple(attrs={"class": "select2"}),
            "documentos_permitidos": forms.SelectMultiple(attrs={"class": "select2"}),
            "txt_mail_confirmacion": forms.Textarea(attrs={"rows": 3}),
            "popup": forms.Textarea(attrs={"rows": 3}),
            "login_BA": forms.Select(choices=[(False, "NO"), (True,"SI")]),
            "vecino_reagendar_cita": forms.Select(choices=[(False, "NO"), (True,"SI")]),
            #"banda_horaria": forms.TextInput(attrs={"placeholder": "Formato horario"}),
            "visibilidad_agenda": forms.NumberInput(attrs={"placeholder": "En días hábiles"}),
            "tiempo_precancelacion": forms.NumberInput(attrs={"placeholder": "En minutos"}),
            }