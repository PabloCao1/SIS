from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.views import PasswordChangeView,LoginView,LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.core.files.base import ContentFile

from .forms import *
from .mixins import *
from .models import *


def set_dark_mode(request):

    if request.method == "POST":
        user = request.user
        user.usuarios.darkmode = not user.usuarios.darkmode
        user.usuarios.save()
        return JsonResponse({"status": "ok"})


class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Ejecutar el método form_valid de la clase base para realizar la validación del formulario
        response = super().form_valid(form)
        
        # Obtener el usuario
        username = form.cleaned_data['username']
        user = form.get_user()

        # Obtener el objeto Usuarios asociado al usuario
        usuario = Usuarios.objects.get(usuario=user)

        # Verificar si la contraseña ingresada es la predeterminada
        if form.cleaned_data['password'] == 'Buenosairesciudad':
            # Incrementar el contador de intentos de inicio de sesión con la contraseña predeterminada
            usuario.intentos_contraseña_predeterminada += 1
            usuario.save()

            # Si ha intentado iniciar sesión con la contraseña predeterminada más de tres veces, bloquear el inicio de sesión
            if usuario.intentos_contraseña_predeterminada >= 3:
                user.is_active = False
                user.save()
                usuario.intentos_contraseña_predeterminada = 0
                usuario.save()
                return render(self.request, "usuario_bloqueado.html")
            else:
                # Si tiene menos de 3 intentos, redirigir al usuario a la página de cambio de contraseña
                messages.warning(self.request, "Por favor, cambia tu contraseña para evitar el bloqueo de la cuenta.")
                return redirect(reverse_lazy('cambiar_password'))

        return response

    def form_invalid(self, form):
        # Obtener el usuario
        username = form.cleaned_data['username']
        user = form.get_user()

        # Verificar si el usuario está desactivado
        if user and not user.is_active:
            # Mostrar un mensaje de error personalizado si el usuario está desactivado
            messages.error(self.request, "Tu cuenta ha sido bloqueada. Por favor, ponte en contacto con el administrador.")
            return self.render_to_response(self.get_context_data(form=form))

        # Si el usuario no está desactivado, continuar con el flujo normal de form_invalid
        return super().form_invalid(form)
        
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
   
   
class UsuariosDetailView(UserPassesTestMixin, DetailView):
    model = Usuarios
    template_name = 'Usuarios/usuarios_detail.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            usuario_actual = self.request.user
            usuario_solicitado = self.get_object().usuario
            # Permitir el acceso si es el mismo usuario o si es un superusuario
            return usuario_actual == usuario_solicitado or self.request.user.is_superuser
        return False


class UsuariosDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):   
    permission_required = ('User.delete_user')   
    model = User
    template_name = 'Usuarios/usuarios_confirm_delete.html'
    success_url= reverse_lazy("usuarios_listar")
    success_message = "El registro fue eliminado correctamente."   


class UsuariosCreateView(CreateView):
    template_name = 'Usuarios/usuarios_form.html'
    form_class = UsuariosCreateForm
    
    def get_success_url(self):
        return reverse_lazy('usuarios_ver', kwargs={'pk': self.object.id})
    

class UsuariosUpdateView(UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = User
    form_class = UsuariosUpdateForm
    template_name = 'Usuarios/usuarios_form.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            usuario_actual = self.request.user.id
            usuario_solicitado = self.get_object().id
            # Permitir el acceso si es el mismo usuario o si es un superusuario
            return usuario_actual == usuario_solicitado or self.request.user.is_superuser
        return False

    def get_success_url(self):
        return reverse_lazy('usuarios_ver', kwargs={'pk': self.object.usuarios.id})

#endregion------------------------------------------------------------------------------------------


#region---------------------------------------------------------------------------------------PASSWORDS


class UsuariosResetPassView(View):
    success_url = reverse_lazy('usuarios_listar')
    template_name = 'Passwords/password_reset.html'

    def get(self, request, *args, **kwargs):
        # Renderizar el template en caso de solicitud GET
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Obtener el usuario
        user_id = kwargs['pk']
        user = get_user_model().objects.get(id=user_id)

        # Establecer la contraseña predeterminada
        user.set_password('Buenosairesciudad')
        user.is_active = True
        user.save()

        # Reiniciar el contador de intentos de inicio de sesión con la contraseña predeterminada
        usuario = Usuarios.objects.get(usuario=user)
        usuario.intentos_contraseña_predeterminada = 0
        usuario.save()

        # Mostrar un mensaje de éxito
        messages.success(request, f"La contraseña se ha restablecido correctamente para el usuario {user}.")

        # Redireccionar a la URL de éxito
        return HttpResponseRedirect(self.success_url)

  
class PerfilChangePassView(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):
    '''
    Vista para que los usuarios logueados (no staff) realicen cambios de clave. 
    Es requisito conocer su clave anterior e introducir una nueva contraseña que cumpla con los requisitos del sistema.
    '''
    template_name='Perfiles/perfil_change_password.html'
    form_class = MyPasswordChangeForm
    success_message = "La contraseña fue modificada con éxito." 
    success_url= reverse_lazy("dashboard") 
    

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
        if form.is_valid():  
            user=form.save()            
            usuario=Usuarios.objects.get(usuario_id=user.id)
            if telefono:
                usuario.telefono = telefono
             # Verificar si la imagen ha cambiado antes de recortarla y guardarla
            if img:
                usuario.imagen = img
            usuario.save()   
            messages.success(self.request, ('Perfil modificado con éxito.'))
        else:
            messages.error(self.request, ('No fue posible modificar el perfil.'))      
        return redirect('usuarios_ver', pk=user.usuarios.id)
  
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
