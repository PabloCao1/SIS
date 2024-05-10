from django import forms
from .models import *

# from Usuarios.models import *


class SedesForm(forms.ModelForm):
    class Meta:
        model = Sedes
        exclude = ()
        widgets = {
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "barrios": forms.SelectMultiple(attrs={"class": "form-control select2"}),
            "tramites": forms.SelectMultiple(attrs={"class": "form-control select2"}),
            "estado": forms.Select(choices=[(True, "Activo"), (False, "Inactivo")]),
        }
        labels = {}


class ServiciosForm(forms.ModelForm):
    class Meta:
        model = Servicios
        exclude = ()
        widgets = {
            "estado": forms.Select(choices=[(True, "Activo"), (False, "Inactivo")]),
        }
        labels = {}


class TramitesForm(forms.ModelForm):
    class Meta:
        model = Tramites
        exclude = ()
        widgets = {
            "turnos": forms.Select(choices=[(True, "Si"), (False, "No")]),
            "espontaneos": forms.Select(choices=[(True, "Si"), (False, "No")]),
            "estado": forms.Select(choices=[(True, "Activo"), (False, "Inactivo")]),
        }
        labels = {"fk_servicio": "Servicio"}
