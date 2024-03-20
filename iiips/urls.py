"""
URL configuration for iiips project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
""" 
from django.contrib import admin
from django.urls import path
from proyectos import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from proyectos.views import UserListView
from proyectos.views import UserDeletedListView
from proyectos.views import editarusuario

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #usuarios
    #path('dashboard/',views.dashboard, name='dashboard'),
    path('listarusuarios', UserListView.as_view(), name='listarusuarios'),
    path('listarusuarioseliminado/', UserDeletedListView.as_view(), name='listarusuarioseliminado'),
    path('listarusuarioseliminado/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editarusuario/<int:user_id>/', views.editarusuario, name='editarusuario'),
    path('registrarusuario/', views.registrarusuario, name='registrarusuario'),
    path('permisos_insuficientes/',views.permisos_insuficientes, name='permisos_insuficientes'),
    #path('reactivar_usuario/<int:user_id>/', views.reactivar_usuario, name='reactivar_usuario'),
    path('usuario/reactivar/<int:user_id>/', views.reactivar_usuario, name='reactivar_usuario'),
    
    
    
    path('', views.home, name='home'),
    path('registrar/', views.registrar, name='registrar'),
    path('logout/',views.signout, name='logout'),
    path('signin/',views.signin, name='signin'),
    
    path('index', views.index, name='index'),
    path('materias/<int:ids>', views.materias, name='materias'),
    path('VerSemestres', views.VerSemestres, name='VerSemestres'),
    
    
   # path('formuno', views.formuno, name='formuno'),
    path('vista/<int:Id_M>', views.vista, name='vista'),
    path('vistas', views.vistas, name='vistas'),
    #proyeto
    path('semestres/crear',views.crear,name='crear'),
    path('semestres/editar/<int:id>',views.editar,name='editar'),
    path('form',views.form,name='form'),
    path('proye',views.proye, name='proye'),
    path('eliminar/<int:id>',views.eliminar,name='eliminar'),
    
    #fases o estapas
    path('FaseEtapa/crearf',views.crearf,name='crearf'),
    path('FaseEtapa/editarf<int:idf>',views.editarf,name='editarf'),
    path('FaseEtapa/formf',views.form,name='formf'),
    path('etapa',views.etapa, name='etapa'),
    path('eliminarf/<int:idf>',views.eliminarf,name='eliminarf'),
    
    #cursos proyecto
    path('curso/crearc',views.crearc,name='crearc'),
    path('curso/editarc/<int:idm>',views.editarc ,name='editarc'),
    path('curso/formc',views.formc,name='formc'),
    path('curso',views.curso, name='curso'),
    path('eliminarm/<int:idm>',views.eliminarm,name='eliminarm'),
    
    #Gestion proyecto
    path('Gestion/crearg',views.crearg,name='crearg'),
    path('Gestion/editarg/<int:idg>',views.editarg ,name='editarg'),
    path('Gestion/formg',views.formg,name='formg'),
    path('gest',views.gest, name='gest'),
    path('eliminarg/<int:idg>',views.eliminarg,name='eliminarg'),
    
    #Semestre proyecto
    path('materia/crearm',views.crears, name='crears'),
    path('materia/editarm/<int:ids>',views.editars, name='editars'),
    path('materia/formm',views.forms, name='forms'),
    path('semest',views.semest, name='semest'),
    path('eliminars/<int:ids>', views.eliminars, name='eliminars'),
    
    #tipo proyecto
    path('Tipo/creart',views.creart, name='creart'),
    path('Tipo/editart/<int:idt>',views.editart, name='editart'),
    path('Tipo/formt',views.formt, name='formt'),
    path('tippo',views.tippo, name='tippo'),
    path('eliminart/<int:idt>', views.eliminart, name='eliminart'),
    
    
    
    path('materiaforn', views.materiaform, name='materiaform'),
    
    
    #paralelos con sus materias
    path('unoA', views.unoA, name='unoA'),
    path('unoB', views.unoB, name='unoB'),
    path('dosA', views.dosA, name='dosA'),
    path('dosB', views.dosB, name='dosB'),
    path('tresA', views.tresA, name='tresA'),
    path('tresB', views.tresB, name='tresB'),
    path('cuatroA', views.cuatroA, name='cuatroA'),
    path('cuatroB', views.cuatroB, name='cuatroB'),
    path('quinto', views.quinto, name='quinto'),
    path('sexto', views.sexto, name='sexto'),
    path('septimo', views.septimo, name='septimo'),
    path('octavo', views.octavo, name='octavo'),
    path('octavoR', views.octavoR, name='octavoR'),
    path('noveno', views.noveno, name='noveno'),
    path('novenoR', views.novenoR, name='novenoR'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
