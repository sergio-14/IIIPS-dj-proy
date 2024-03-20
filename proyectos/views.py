from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .import models 
from .forms import PForm, FForm, TForm, MForm, SForm, GForm
from django.contrib.auth.decorators import permission_required

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SuperuserPermissionForm


from django.views.generic import ListView

from django.contrib.auth.forms import UserChangeForm
from .forms import RegistrationForm
from django.contrib import messages  # Importe a biblioteca de mensagens
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission

from django.core.paginator import Paginator
# Create your views here.

class UserListView(ListView):
    model = User
    template_name = 'listarusuarios.html'
    context_object_name = 'users'

    def get_queryset(self):
        # Filtrar solo usuarios activos
        return User.objects.filter(is_active=True)

class UserDeletedListView(ListView):
    model = User
    template_name = 'listarusuarioseliminado.html'  # Nombre de la plantilla HTML para la lista de usuarios eliminados
    context_object_name = 'deleted_users'  # Nombre del objeto que representará la lista de usuarios eliminados en la plantilla
    queryset = User.objects.filter(is_active=False)  # Consulta para recuperar usuarios eliminados
    
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active']

def check_permissions(user):
    return user.is_superuser or user.is_staff

def permisos_insuficientes(request):
    return render(request, 'permisos_insuficientes.html')

@user_passes_test(check_permissions, login_url='/permisos_insuficientes/')
def dashboard(request):
    context = {'usuario_actual': request.user}
    return render(request, 'dashboard.html',context)

@login_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False  # Marcar el usuario como inactivo
    user.save()  # Guardar el cambio
    messages.success(request, 'Usuario desactivado exitosamente.')
    return redirect('listarusuarios')  # Redirigir a la lista de usuarios o a donde desees
        
@permission_required('permiso_especifico')   
def editarusuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            # Obtener los IDs de permisos seleccionados del formulario
            selected_perm_ids = request.POST.getlist('permissions')
            # Limpiar los permisos actuales
            usuario.user_permissions.clear()
            # Asignar los nuevos permisos al usuario
            for perm_id in selected_perm_ids:
                perm = Permission.objects.get(id=perm_id)
                usuario.user_permissions.add(perm)
            usuario.save()
            return redirect('listarusuarios')
    else:
        form = CustomUserChangeForm(instance=usuario)
    # Obtener todos los permisos y los permisos actuales del usuario
    all_perms = Permission.objects.all()
    user_perms = usuario.user_permissions.all()
    return render(request, 'editarusuario.html', {
        'form': form,
        'user': usuario,
        'all_perms': all_perms,
        'user_perms': user_perms
    })
    
@login_required
def registrarusuario(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_superuser = form.cleaned_data.get('is_superuser')
            user.is_staff = form.cleaned_data.get('is_staff')
            user.is_active = form.cleaned_data.get('is_active')
            user.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('listarusuarios')

    else:
        form = RegistrationForm()

    return render(request, 'registrarusuario.html', {'form': form})

@login_required
def reactivar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    # Redirige a la vista que muestra la lista de usuarios eliminados
    return redirect('listarusuarioseliminado')

# def editarusuario(request, usuario_id):
#     # Obtén el usuario que deseas editar
#     usuario = User.objects.get(id=usuario_id)

#     # Verifica si la solicitud es un POST (es decir, si se envió el formulario)
#     if request.method == 'POST':
#         # Crea una instancia del formulario con los datos de la solicitud
#         form = SuperuserPermissionForm(request.POST, instance=usuario)
#         # Guarda los cambios si el formulario es válido
#         if form.is_valid():
#             form.save()
#     else:
#         # Si no es un POST, crea una instancia del formulario con los datos actuales del usuario
#         form = SuperuserPermissionForm(instance=usuario)

#     return render(request, 'formuser.html', {'form': form, 'usuario': usuario})

class CustomUserAdmin(UserAdmin):
    form = SuperuserPermissionForm

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Create your views here.


def home(request):
    return render(request, 'home.html')

@login_required
def registrar(request):
    if request.method == 'GET':
        return render(request, 'registrar.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'registrar.html', {
                    'form': UserCreationForm,
                    "error": 'User ya existe'
                })
        return render(request, 'registrar.html', {
            'form': UserCreationForm,
            "error": 'la contraseña no concide'
        })


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario y contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('home')
       
def index(request):
    Id_Materia=models.T_Materia.objects.get(pk=3)
    return render(request, 'semestres/index.html',{
        'Id_Materia' : Id_Materia
    })

def formuno(request):
    return render(request, 'unesemestres/formuno.html')

#def vista(request, Id_M):
   # Id_Materia=models.T_Materia.objects.get(pk=Id_M)
   # datos=models.T_Proyectos.objects.filter(T_Materia=Id_Materia)
  #  return render(request, 'semestres/vista.html',{'datos': datos,})

def vista(request, Id_M):
    Id_Materia=models.T_Materia.objects.get(pk=Id_M)
    datos=models.T_Proyectos.objects.filter(T_Materia=Id_Materia)
    paginator = Paginator(datos,1)
    page_number = request.GET.get('page')  # Obtén el número de página de la URL
    datos = paginator.get_page(page_number)  # Obtiene la página actual
    
    return render(request, 'semestres/vista.html',{'datos': datos,})


def vistas(request):
    semestres = models.T_Semestre.objects.all()
    
    return render(request, 'semestres/vistas.html',{
        'semestres': semestres,
    })

def materias(request,ids):
    semestre = models.T_Semestre.objects.get(Id_Semestre= ids)
    materiasSemestre= models.T_Materia.objects.filter(T_Semestre=semestre)
    return render(request, 'paralelos/materias.html',{
        'semestre': semestre,
        'materias':materiasSemestre,   
    })
    
@login_required  
def VerSemestres(request):
    return render(request, 'paralelos/VerSemestres.html')


# poryectos
@login_required
def crear(request):
    formulario = PForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('proye')
    return render(request, 'semestres/crear.html',{'formulario': formulario})


# mform = models.T_Materia.objects.get(Id_Materia=idm)
#     formularioc = MForm(request.POST or None, request.FILES or None, instance=mform)
#     # formularioc = MForm()
#     if formularioc.is_valid() and request.POST:
#         formularioc.save()
#         return redirect('proye')
#     #return render(request,'curso/editarc.html')
#     return render(request, 'curso/editarc.html',{'formularioc': formularioc})
@login_required
def editar(request, id):
    programa = models.T_Proyectos.objects.get(Id_Proyect=id)
    formulario = PForm(request.POST or None, request.FILES or None, instance=programa)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('proye')
    return render(request, 'semestres/editar.html',{'formulario': formulario})
@login_required
def form(request):
    return render(request, 'semestres/form.html')
@login_required
def proye(request):
     programa = models.T_Proyectos.objects.all()
     return render(request, 'semestres/indexgeneral.html',{'programa': programa})
@login_required 
def materiaform(request):
     mtf = models.T_Semestre.objects.all()
     return render(request, 'materia1/formulariomateria.html',{'mtf': mtf})
@login_required
def eliminar(request, id):
    programa = models.T_Proyectos.objects.get(Id_Proyect=id)
    programa.delete()
    return redirect('proye')

# fase del proyecto
@login_required
def crearf(request):
    formulariof = FForm(request.POST or None, request.FILES or None)
    if formulariof.is_valid():
        formulariof.save()
        return redirect('etapa')
    return render(request, 'FaseEtapa/crearf.html',{'formulariof': formulariof})
@login_required
def editarf(request, idf):
    fform = models.T_Fase_proyecto.objects.get(Id_fase=idf)
    formulariof = FForm(request.POST or None, request.FILES or None, instance=fform)
    if formulariof.is_valid() and request.POST:
        formulariof.save()
        return redirect('etapa')
    return render(request, 'FaseEtapa/editarf.html',{'formulariof': formulariof})
@login_required
def formf(request):
    return render(request, 'FaseEtapa/formf.html')
@login_required
def etapa(request):
    fform = models.T_Fase_proyecto.objects.all()
    return render(request, 'semestres/etapa.html',{'fform': fform})
@login_required
def eliminarf(request, idf):
    fform = models.T_Fase_proyecto.objects.get(Id_fase=idf)
    fform.delete()
    return redirect('etapa')



# cursos proyecto
@login_required
def crearc(request):
    formularioc = MForm(request.POST or None, request.FILES or None)
    if formularioc.is_valid():
        formularioc.save()
        return redirect('curso')
    return render(request, 'curso/crearc.html',{'formularioc': formularioc})
@login_required
def editarc(request,idm):
    mform = models.T_Materia.objects.get(Id_Materia=idm)
    formularioc = MForm(request.POST or None, request.FILES or None, instance=mform)
    # formularioc = MForm()
    if formularioc.is_valid() and request.POST:
        formularioc.save()
        return redirect('curso')
    #return render(request,'curso/editarc.html')
    return render(request, 'curso/editarc.html',{'formularioc': formularioc})
@login_required
def formc(request):
    return render(request, 'curso/formc.html')
@login_required
def curso(request):
    mform = models.T_Materia.objects.all()
    return render(request, 'semestres/curso.html',{'mform': mform})
@login_required
def eliminarm(request, idm):
    mform = models.T_Materia.objects.get(Id_Materia=idm)
    mform.delete()
    return redirect('curso')


# Gestion proyecto
@login_required
def crearg(request):
    formulariog = GForm(request.POST or None, request.FILES or None)
    if formulariog.is_valid():
        formulariog.save()
        return redirect('gest')
    return render(request, 'Gestion/crearg.html',{'formulariog': formulariog})
@login_required
def editarg(request, idg):
    gform = models.T_Gestion.objects.get(Id_Ges=idg)
    formulariog = GForm(request.POST or None, request.FILES or None, instance=gform)
    if formulariog.is_valid() and request.POST:
        formulariog.save()
        return redirect('gest')
    return render(request, 'Gestion/editarg.html',{'formulariog': formulariog})
@login_required
def formg(request):
    return render(request, 'Gestion/formg.html')
@login_required
def gest(request):
    gform = models.T_Gestion.objects.all()
    return render(request, 'semestres/gestion.html',{'gform': gform})
@login_required
def eliminarg(request, idg):
    gform = models.T_Gestion.objects.get(Id_Ges=idg)
    gform.delete()
    return redirect('gest')



# semestre proyecto
@login_required
def eliminars(request, ids):
    sform = models.T_Semestre.objects.get(Id_Semestre = ids)
    sform.delete()
    return redirect('semest')
@login_required   
def crears(request):
    formularios = SForm(request.POST or None, request.FILES or None)
    if formularios.is_valid():
        formularios.save()
        return redirect('semest')
    return render(request, 'materia/crearm.html',{'formularios': formularios})
@login_required
def editars(request, ids):
    sform = models.T_Semestre.objects.get(Id_Semestre=ids)
    formularios = SForm(request.POST or None, request.FILES or None, instance=sform)
    if formularios.is_valid() and request.POST:
        formularios.save()
        return redirect('semest')
    return render(request, 'materia/editarm.html',{'formularios': formularios})
@login_required
def forms(request):
    return render(request, 'materia/formm.html')
@login_required
def semest(request):
    sform = models.T_Semestre.objects.all()
    return render(request, 'semestres/semest.html',{'sform': sform})

# tipo proyecto
@login_required
def creart(request):
    formulariot = TForm(request.POST or None, request.FILES or None)
    if formulariot.is_valid():
        formulariot.save()
        return redirect('tippo')
    return render(request, 'Tipo/creart.html',{'formulariot': formulariot})
@login_required
def editart(request, idt):
    tform = models.T_Tipo_Proyecto.objects.get(Id_tipo=idt)
    formulariot = TForm(request.POST or None, request.FILES or None, instance=tform)
    if formulariot.is_valid() and request.POST:
        formulariot.save()
        return redirect('tippo')
    return render(request, 'Tipo/editart.html',{'formulariot': formulariot})
@login_required
def formt(request):
    return render(request, 'Tipo/formt.html')
@login_required
def tippo(request):
    tform = models.T_Tipo_Proyecto.objects.all()
    return render(request, 'semestres/tipo.html',{'tform': tform})
@login_required
def eliminart(request, idt):
    sform = models.T_Tipo_Proyecto.objects.get(Id_tipo = idt)
    sform.delete()
    return redirect('tippo')


#paralelos con materias 
@login_required
def unoA(request):
    return render(request, 'paralelos/unoA.html')
@login_required
def unoB(request):
    return render(request, 'paralelos/unoB.html')
@login_required
def dosA(request):
    return render(request, 'paralelos/dosA.html')
@login_required
def dosB(request):
    return render(request, 'paralelos/dosB.html')
@login_required
def tresA(request):
    return render(request, 'paralelos/tresA.html')
@login_required
def tresB(request):
    return render(request, 'paralelos/tresB.html')

def cuatroA(request):
    return render(request, 'paralelos/cuatroA.html')

def cuatroB(request):
    return render(request, 'paralelos/cuatroB.html')

def quinto(request):
    return render(request, 'paralelos/quinto.html')

def sexto(request):
    return render(request, 'paralelos/sexto.html')

def septimo(request):
    return render(request, 'paralelos/septimo.html')

def octavo(request):
    return render(request, 'paralelos/octavo.html')

def octavoR(request):
    return render(request, 'paralelos/octavoR.html')

def noveno(request):
    return render(request, 'paralelos/noveno.html')

def novenoR(request):
    return render(request, 'paralelos/novenoR.html')






