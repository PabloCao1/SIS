from django import forms
from django.contrib.auth.models import User,Group, Permission
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm, SetPasswordForm,PasswordResetForm
from .validators import MaxSizeFileValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator
from utils.utils import recortar_imagen
from django.forms.widgets import CheckboxInput

from .models import *

usuarios=Usuarios.objects.all()

    
class UsuariosCreateForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    imagen = forms.ImageField(required=False)
    cuil = forms.IntegerField()
    telefono = forms.CharField(max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('imagen', 'cuil', 'telefono', 'groups')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs['class'] = 'select2'  # Aplicar clase select2 si deseas un estilo especial
        self.fields['groups'].label = "Grupos de usuario"

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            usuario = Usuarios.objects.create(
                usuario=user,
                imagen= recortar_imagen(self.cleaned_data['imagen']),
                cuil=self.cleaned_data['cuil'],
                telefono=self.cleaned_data['telefono']
            )
            grupos = self.cleaned_data.get('groups')
            if grupos:
                user.groups.set(grupos)
        return user

      
class UsuariosUpdateForm(UserChangeForm):
    imagen      = forms.ImageField(validators=[MaxSizeFileValidator(max_file_size=2)],required=False)
    telefono    = forms.IntegerField(help_text="Solo valores numéricos",required=False,widget=forms.NumberInput(attrs={'name': 'telefono',}))
    cuil = forms.CharField(required=True, validators=[MinLengthValidator(11), MaxLengthValidator(11)], widget=forms.TextInput(attrs={'name': 'cuil',}),)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email' ,'imagen', 'cuil', 'telefono', 'groups','is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuario=(usuarios.get(usuario_id=self.instance.pk))
        self.fields['groups'].widget.attrs['class'] = 'select2'
        self.fields['is_active'].widget = forms.Select(choices=[(True,'SI'),(False,'NO'),])
        self.fields.pop('password')  # Eliminar el campo de contraseña
        self.fields['telefono'].initial = usuario.telefono
        self.fields['imagen'].initial = usuario.imagen
        self.fields['cuil'].initial = usuario.cuil 
        self.fields['telefono'].label = "Teléfono"  
        self.fields['groups'].label = "Grupos de usuario" 
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            usuario, created = Usuarios.objects.get_or_create(usuario=user)
            usuario.imagen = recortar_imagen(self.cleaned_data['imagen'])
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
    cuil    = forms.IntegerField(required=True,widget=forms.NumberInput(attrs={'name': 'cuil',}))
    telefono    = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'name': 'telefono',}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefono'].initial = (usuarios.get(usuario_id=self.instance.pk)).telefono
        self.fields['cuil'].initial = (usuarios.get(usuario_id=self.instance.pk)).cuil
        self.fields['imagen'].initial = (usuarios.get(usuario_id=self.instance.pk)).imagen
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None

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


class MySetPasswordFormm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget = forms.PasswordInput()
        self.fields["new_password2"].widget = forms.PasswordInput()


class MyResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget = forms.EmailInput(attrs={'class': 'border-0 font-weight-bold text-center','readonly': True})

