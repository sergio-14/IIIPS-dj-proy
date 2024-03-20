from django.contrib import admin
from .models import T_Fase_proyecto 
from .models import T_Tipo_Proyecto
from .models import T_Gestion
from .models import T_Proyectos
from .models import T_Semestre
from .models import T_Materia

# Register your models here.
admin.site.register(T_Fase_proyecto)
admin.site.register(T_Tipo_Proyecto)
admin.site.register(T_Gestion)
admin.site.register(T_Proyectos)
admin.site.register(T_Semestre)
admin.site.register(T_Materia)

