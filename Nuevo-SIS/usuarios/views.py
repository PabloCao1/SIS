from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView,LoginView,LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO  # Import BytesIO


from .forms import *
from .mixins import *
from .models import *


def set_dark_mode(request):

    if request.method == "POST":
        user = request.user
        user.usuarios.darkmode = not user.usuarios.darkmode
        user.usuarios.save()
        return JsonResponse({"status": "ok"})


class CustomLogoutView(LoginRequiredMixin, LogoutView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, "Sesión cerrada con éxito.")
        return response



#region---------------------------------------------------------------------------------------USUARIOS
class UsuariosListView(PermissionRequiredMixin,ListView ):    
    permission_required = ['Usuarios.view_usuarios',]   
    model = Usuarios

    #Funcion de busqueda
    def get_queryset(self):
        query = self.request.GET.get('busqueda')
        if query:
            # Separa el término de búsqueda en nombre y apellido
            terminos = query.split()
            nombre = terminos[0]
            apellido = terminos[-1]

            object_list = self.model.objects.filter(
                Q(usuario__username__icontains=query) |
                Q(usuario__first_name__icontains=nombre) & Q(usuario__last_name__icontains=apellido) |
                Q(usuario__first_name__icontains=query) |
                Q(usuario__last_name__icontains=query) |
                Q(usuario__email__icontains=query) |
                Q(telefono__icontains=query)
            ).distinct()
        else:
            object_list = self.model.objects.all().exclude(usuario_id__is_superuser =True)
        return object_list
   
   
class UsuariosDetailView(UserPassesTestMixin,DetailView):
    permission_required = ['Usuarios.view_usuarios',] 
    model = Usuarios
    template_name = 'Usuarios/usuarios_detail.html'

    def test_func(self):
    # accede a la vista de detalle si es admin o si es el mismo usuario
       if self.request.user.is_authenticated:
            usuario_actual = self.request.user.id
            usuario_solicitado= int(self.kwargs['pk'])
            if (usuario_actual == usuario_solicitado) or self.request.user.has_perm('Usuarios.rol_admin') or self.request.user.has_perm('auth_user.view_user'):
                return True
       else:
           return False 


class UsuariosDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):   
    permission_required = ('Usuarios.delete_usuarios')   
    model = Usuarios
    template_name = 'Usuarios/usuarios_confirm_delete.html'
    success_url= reverse_lazy("usuarios_listar")
    success_message = "El registro fue eliminado correctamente."   


class UsuariosCreateView(CreateView):
    template_name = 'Usuarios/usuarios_form.html'
    form_class = UsuariosCreateForm
    
    def get_success_url(self):
        return reverse_lazy('usuarios_ver', kwargs={'pk': self.object.usuarios.id})
    
class UsuariosUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = ('Usuarios.change_usuarios')
    model = User
    form_class = UsuariosUpdateForm
    template_name = 'Usuarios/usuarios_form.html'

    def get_success_url(self):
        return reverse_lazy('usuarios_ver', kwargs={'pk': self.object.usuarios.id})

#endregion------------------------------------------------------------------------------------------


#region---------------------------------------------------------------------------------------PASSWORDS

class UsuariosResetPassView(PermissionRequiredMixin,SuccessMessageMixin,PasswordResetView):
    '''
    Permite al usuario staff resetear la clave a otros usuarios del sistema mediante el envío de un token por mail. 
    IMPORTANTE: el mail  al que se envía el token de recupero debe coincidir con el mail que el usuario tiene 
    almacenado en su perfil, por lo cual es imprescindible chequear que sea correcto.

    De la documentación de Django: 
        Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
    '''
    permission_required = ('User.change_user')   
    template_name='Passwords/password_reset.html'
    form_class = MyResetPasswordForm
    success_url = reverse_lazy('usuarios_listar')
    success_message = "Mail de reseteo de contraseña enviado con éxito."

    def get_context_data(self, *args, **kwargs):
        context = super(UsuariosResetPassView, self).get_context_data(**kwargs)
        user_id =self.kwargs['pk']
        user = User.objects.get(id=user_id)
        usuario = Usuarios.objects.get(usuario_id=user_id)
        email=user.email
        context['email'] = email
        context['user'] = user
        return context
    


#endregion


#region---------------------------------------------------------------------------------------PERFILES DE USUARIOS     

class PerfilUpdateView(UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    '''
    Vista para que los usuarios logueados (no staff) realicen cambios en sus datos de perfil.
    De la tabla USER: Nombre de usuario, Nombre, Apellido o email.
    De la tabla USUARIOS(extensión del modelo USER): telefono.
    '''
    model = User
    form_class = PerfilUpdateForm      
    template_name = 'Perfiles/perfil_update_form.html'
    success_message = "Perfil editado con éxito."  

    def test_func(self):
        # accede a la vista si es el mismo usuario
        if self.request.user.is_authenticated:
                usuario_actual = self.request.user.id
                usuario_solicitado= int(self.kwargs['pk'])
                if (usuario_actual == usuario_solicitado):
                    return True
        else:
            return False 

    def form_valid(self, form): 
        img=self.request.FILES.get('imagen')
        telefono = form.cleaned_data['telefono']    
        cuil = form.cleaned_data['cuil']    
        if form.is_valid():  
            user=form.save()            
            usuario=Usuarios.objects.get(usuario_id=user.id)
            if cuil:
                usuario.cuil = cuil
            if telefono:
                usuario.telefono = telefono
             # Verificar si la imagen ha cambiado antes de recortarla y guardarla
            if img:
                imagen = Image.open(img)
                tamano_minimo = min(imagen.width, imagen.height)
                area = (0, 0, tamano_minimo, tamano_minimo)
                imagen_recortada = imagen.crop(area)
                buffer = BytesIO()
                imagen_recortada.save(buffer, format='PNG')
                usuario.imagen.save(img.name, ContentFile(buffer.getvalue()))
            usuario.save()   
            messages.success(self.request, ('Perfil modificado con éxito.'))
        else:
            messages.error(self.request, ('No fue posible modificar el perfil.'))      
        return redirect('usuarios_ver', pk=user.id)
    
class PerfilChangePassView(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):
    '''
    Vista para que los usuarios logueados (no staff) realicen cambios de clave. 
    Es requisito conocer su clave anterior e introducir una nueva contraseña que cumpla con los requisitos del sistema.
    '''
    template_name='Perfiles/perfil_change_password.html'
    form_class = MyPasswordChangeForm
    success_message = "La contraseña fue modificada con éxito."  
    

#endregion


#region---------------------------------------------------------------------------------------Grupos de usuario

class GruposListView(PermissionRequiredMixin,ListView ):    
    permission_required = ['Group.view_group',]    
    model = Group
    template_name = 'Grupos/grupos_list.html'

    #Funcion de busqueda
    def get_queryset(self):
        query = self.request.GET.get('busqueda')
        if query:
            object_list = self.model.objects.filter(
                Q(permissions__codename__icontains=query) |
                Q(name__icontains=query) 
            ).distinct()
        else:
            object_list = self.model.objects.all().order_by('name')
        return object_list
   
   
class GruposDetailView(PermissionRequiredMixin,DetailView):
    permission_required = ['Group.view_group',]  
    model = Group
    template_name = 'Grupos/grupos_detail.html'


class GruposDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):   
    permission_required = ['Group.delete_group',]   
    model = Group
    template_name = 'Grupos/grupos_confirm_delete.html'
    success_url= reverse_lazy("grupos_listar")
    success_message = "El registro fue eliminado correctamente."  


class GruposCreateView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):    
    permission_required = ['Group.add_group',]   
    model = Group
    form_class = GruposUsuariosForm
    template_name = 'Grupos/grupos_form.html'
    success_message = "%(name)s fue registrado correctamente."  
        
    def form_invalid(self, form):
        messages.error(self.request,"Ya existe un grupo con esos permisos.")
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('grupos_ver', kwargs={'pk': self.object.id})



class GruposUpdateView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    permission_required = ('Group.change_group')   
    model = Group
    form_class = GruposUsuariosForm  
    template_name = 'Grupos/grupos_form.html'  
    success_message = "%(name)s fue editado correctamente"   

        
    def form_invalid(self, form):
        messages.error(self.request,"Ya existe un grupo con esos permisos.")
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('grupos_ver', kwargs={'pk': self.object.id})
#endregion------------------------------------------------------------------------------------------
