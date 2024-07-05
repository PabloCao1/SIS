from django import forms
from django.forms import ValidationError
from .validators import *
from .models import *
from .choices import *


class BaseFechaDesdeHastaForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        fecha_desde = cleaned_data.get("fecha_desde")
        fecha_hasta = cleaned_data.get("fecha_hasta")

        if fecha_desde.year < 2000:
            raise forms.ValidationError("La FECHA debe ser posterior al año 2000.")

        if fecha_desde and fecha_hasta:
            if fecha_hasta.year < 2000:
                raise forms.ValidationError("La FECHA debe ser posterior al año 2000.")

            if fecha_hasta < fecha_desde:
                raise forms.ValidationError(
                    "La FECHA HASTA debe ser posterior a la FECHA DESDE."
                )

        return cleaned_data


# --------- FORMULARIOS EmpleadoS ---------
class EmpleadoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

    def clean_CUIT(self):
        CUIT = self.cleaned_data["CUIT"]
        if len(str(CUIT)) != 11:
            raise forms.ValidationError("El número debe poseer 11 caracteres")

        # Verifica si el objeto ya existe en la base de datos
        if self.instance.pk is None:  # Solo durante la creación
            existe = Empleado.objects.filter(CUIT=CUIT).exists()
            if existe:
                raise forms.ValidationError("Este CUIT ya se encuentra en la base.")
        return CUIT

    foto = forms.ImageField(
        required=False,
        label="Foto perfil",
        validators=[MaxSizeFileValidator(max_file_size=2)],
    )

    class Meta:
        model = Empleado
        fields = "__all__"
        widgets = {
            
            "GO_equipo": forms.Select(choices=CHOICE_GO_EQUIPO),
            "m2m_tareas": forms.SelectMultiple(attrs={"class": "select2"}),
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),            
            "sexo": forms.Select(choices=CHOICE_SEXO),
            "estado_civil": forms.Select(choices=CHOICE_ESTADO_CIVIL),
            "calle": forms.TextInput(attrs={"placeholder": "Calle"}),
            "ciudad": forms.TextInput(attrs={"placeholder": "Ciudad"}),
            "provincia": forms.Select(
                choices=CHOICE_PROVINCIAS, attrs={"placeholder": "Provincia"}
            ),
            "CP": forms.TextInput(attrs={"placeholder": "Código Postal"}),
            "piso": forms.TextInput(attrs={"placeholder": "Piso"}),
            "altura": forms.NumberInput(attrs={"placeholder": "Altura"}),
            "departamento": forms.TextInput(attrs={"placeholder": "Depto"}),
            "comuna": forms.Select(choices=CHOICE_COMUNA),
            "tipo_contratacion": forms.Select(choices=CHOICE_TIPO_CONTRATACION),
            "activo": forms.HiddenInput(),
            "en_comision": forms.Select(choices=[(True,"SI"), (False, "NO")]),
            "remoto": forms.Select(choices=[(True,"SI"), (False, "NO")]),
            "gremio": forms.Select(choices=[(True,"SI"), (False, "NO")]),
            "discapacidad": forms.Select(choices=[(True,"SI"), (False, "NO")]),
            "capacitacion_polivalente": forms.Select(choices=[(True,"SI"), (False, "NO")]),
            "ult_eval_desemp": forms.Select(choices=CHOICE_EVAL_DESEMPENIO),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
            "niv_educativo": forms.Select(choices=CHOICE_NIVEL_EDUCATIVO),
            "vacaciones_anuales": forms.NumberInput(attrs={"placeholder": "Días"})
            }


class EmpleadoTraspasosForm(BaseFechaDesdeHastaForm):
    class Meta:
        model = EmpleadoTraspaso
        fields = ["fk_empleado", "tipo", "sede", "motivo", "fecha_desde", "fecha_hasta"]
        widgets = {
            # "fk_empleado": forms.Select(attrs={"class": "form-control"}),
            # "tipo": forms.Select(attrs={"class": "form-control"}),
            # "sede": forms.TextInput(attrs={"class": "form-control"}),
            # "motivo": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_desde": forms.DateInput(
                attrs={"type": "date"}
            ),
            "fecha_hasta": forms.DateInput(
                attrs={"type": "date"}
            ),
            "fk_empleado": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Empleado.objects.filter(id=self.instance.id).exists():
            self.fields["fk_empleado"].initial = Empleado.objects.get(
                id=self.instance.id
            )


class EmpleadoLicenciaForm(BaseFechaDesdeHastaForm):
    class Meta:
        model = EmpleadoLicencia
        fields = ["fk_empleado", "tipo", "motivo", "fecha_desde", "fecha_hasta"]
        widgets = {
            "fecha_desde": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "fecha_hasta": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "fk_empleado": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Empleado.objects.filter(id=self.instance.id).exists():
            self.fields["fk_empleado"].initial = Empleado.objects.get(
                id=self.instance.id
            )


class EmpleadoEventoForm(forms.ModelForm):
    class Meta:
        model = EmpleadoEvento
        fields = ["evento", "asistio", "inscripto", "empleado"]
        widgets = {
            "asistio": forms.Select(
                choices=[(None, ""), (True, "SI"), (False, "NO")],
                attrs={"class": "form-control"},
            ),
            "evento": forms.Select(attrs={"class": "form-control"}),
            "inscripto": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "empleado": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["asistio"].label = "Asistió"
        self.fields["evento"].queryset = Evento.objects.all()
        if Empleado.objects.filter(id=self.instance.id).exists():
            self.fields["empleado"].initial = Empleado.objects.get(id=self.instance.id)


# --------- FORMULARIOS Evento -------------


class EventoForm(forms.ModelForm):

    class Meta:
        model = Evento
        fields = [
            'fk_tipo',
            "flyer",
            "nombre",
            "fecha",
            "modalidad",
            "horario",
            "duracion",
            "lugar",
            "link",
            "descripcion",
        ]
        widgets = {
            # "flyer": forms.HiddenInput(),
            "fecha": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "horario": forms.TimeInput(attrs={"type": "time"}),
            "duracion": forms.TextInput(
                attrs={"placeholder": "Ej: 6 encuentros semanales de 2 Hs."}
            ),
            "modalidad": forms.Select(choices=CHOICE_EVENTO_MODALIDAD),
            "descripcion": forms.Textarea(attrs={"rows": "4"}),
        }
        labels = {"descripcion": "Descripción", "duracion": "Duración"}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fk_tipo"].queryset = TipoEvento.objects.all()
