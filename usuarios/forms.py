from django import forms
from django.contrib.auth.models import User,Group, Permission
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm, SetPasswordForm,PasswordResetForm
from .validators import MaxSizeFileValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.forms.widgets import CheckboxInput

from .models import *

usuarios=Usuarios.objects.all()


class CuilField(forms.CharField):
    default_validators = [RegexValidator(regex=r'^\d{11}$', message="El CUIL debe contener 11 dígitos.")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['maxlength'] = 11
        self.widget.attrs['placeholder'] = 'Ej: 20303344550'
        self.widget.attrs['class'] = 'cuil-mask'  # Agregar una clase CSS para identificar el campo de CUIL

class UsuariosCreateForm(forms.ModelForm):
    username = CuilField(
        help_text="Ingrese número de CUIL. Debe contener 11 dígitos.",
        label="CUIL"
    )
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = Usuarios
        fields = ('username', 'imagen', 'telefono', 'groups')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs['class'] = 'select2'  
        self.fields['groups'].label = "Grupos de usuario"

    def clean_username(self):
        username = self.cleaned_data['username']
        # Verificar si el CUIL ya existe en el sistema
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El CUIL ya está en uso.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            usuario = Usuarios.objects.create(
                usuario=user,
                imagen= self.cleaned_data['imagen'],
                cuil=self.cleaned_data['cuil'],
                telefono=self.cleaned_data['telefono']
            )
        
        # Asignar una contraseña predeterminada
        raw_password = 'Buenosairesciudad'
        user.set_password(raw_password)
        user.save()

        # Crear el objeto Usuarios asociado
        usuario = super().save(commit=False)
        usuario.usuario = user
        usuario.save()

        # Asignar los grupos
        grupos = self.cleaned_data.get('groups')
        if grupos:
            user.groups.set(grupos)

        return usuario

class UsuariosUpdateForm(UserChangeForm):
    imagen      = forms.ImageField(validators=[MaxSizeFileValidator(max_file_size=2)],required=False)
    telefono    = forms.IntegerField(help_text="Solo valores numéricos",required=False,widget=forms.NumberInput(attrs={'name': 'telefono',}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    username = CuilField(
        help_text="Ingrese número de CUIL. Debe contener 11 dígitos.",
        label="CUIL"
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email' ,'imagen', 'telefono', 'groups','is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuario=(usuarios.get(usuario_id=self.instance.id))
        self.fields['groups'].widget.attrs['class'] = 'select2'
        self.fields['is_active'].widget = forms.Select(choices=[(True,'SI'),(False,'NO'),])
        self.fields.pop('password')  # Eliminar el campo de contraseña
        self.fields['telefono'].initial = usuario.telefono
        self.fields['imagen'].initial = usuario.imagen
        self.fields['telefono'].label = "Teléfono"  
        self.fields['groups'].label = "Grupos de usuario" 
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            usuario, created = Usuarios.objects.get_or_create(usuario=user)
            usuario.imagen = self.cleaned_data['imagen']
            usuario.cuil = self.cleaned_data['cuil']
            usuario.telefono = self.cleaned_data['telefono']
            usuario.save()

            grupos = self.cleaned_data.get('groups')
            if grupos:
                user.groups.set(grupos)
        return user

class PerfilUpdateForm(UserChangeForm):
    '''
    Formulario para usuario actual
    '''
    imagen = forms.ImageField(required=False, label="Foto Perfil", validators=[MaxSizeFileValidator(max_file_size=2)])  
    telefono    = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'name': 'telefono',}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefono'].initial = (usuarios.get(usuario_id=self.instance.pk)).telefono
        self.fields['imagen'].initial = (usuarios.get(usuario_id=self.instance.pk)).imagen
        self.fields['username'].disabled = True 
        for fieldname in ['username']:
            self.fields[fieldname].help_text = 'No es posible modificar este campo.'

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        

class GruposUsuariosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar los grupos predeterminados de Django
        self.fields['permissions'].queryset = Permission.objects.filter(content_type__app_label__in=['rrhh', 'sedes', 'tktGOPA'])

    def clean_name(self):
        name = self.cleaned_data['name']
        if Group.objects.filter(name=name).exists():
            raise forms.ValidationError("Ya existe un grupo con ese nombre.")
        return name

    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions'    :  forms.SelectMultiple(attrs={'class': 'select2 w-100'},),
        }


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput()
        self.fields["new_password1"].widget = forms.PasswordInput()
        self.fields["new_password2"].widget = forms.PasswordInput()

