
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from typing import Any
from django.db import models

# Create your models here.
class T_Tipo_Proyecto(models.Model):
    Id_tipo=models.AutoField(primary_key=True)
    Tipo= models.CharField(max_length=100, verbose_name='Tipo')
    
    def __str__(self):
        return self.Tipo


class T_Fase_proyecto(models.Model):
    Id_fase= models.AutoField(primary_key=True)
    Fase=models.CharField(max_length=100,verbose_name='Fase')
    
    def __str__(self):
        return self.Fase 

class T_Gestion(models.Model):
    Id_Ges=models.AutoField(primary_key=True)
    Gestion= models.CharField(max_length=100,verbose_name='Nom_Gestion')
    
    def __str__(self):
        return self.Gestion
    
class T_Semestre(models.Model):
    Id_Semestre= models.AutoField(primary_key=True)
    Semestre=models.CharField(max_length=100,verbose_name='Semestre')
    
    def __str__(self):
        return self.Semestre 
    
class T_Materia(models.Model):
    Id_Materia= models.AutoField(primary_key=True)
    Materia=models.CharField(max_length=100,verbose_name='Materia')
    T_Semestre=models.ForeignKey(T_Semestre, on_delete=models.CASCADE, verbose_name="Semestre")
    def __str__(self):
        return self.Materia

class T_Proyectos(models.Model):
    Id_Proyect=models.AutoField(primary_key=True)
    Titulo= models.CharField(max_length=150,verbose_name='Titulo')
    Fecha_Inicio= models.DateField(auto_now=False, auto_now_add=False)
    Fecha_Finalizacion=models.DateField(auto_now=False, auto_now_add=False)
    Descripcion=models.TextField(verbose_name='Descripcion', blank=True)
    Documentacion=models.FileField(upload_to='Documento/',verbose_name='Documentacion',null=True)
    Imagen=models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null= True)
    T_Fase_proyecto=models.ForeignKey(T_Fase_proyecto, on_delete=models.CASCADE,verbose_name='Fase del Proyecto')
    T_Gestion=models.ForeignKey(T_Gestion, on_delete=models.CASCADE, verbose_name='Gestion')
    T_Tipo_Proyecto=models.ForeignKey(T_Tipo_Proyecto, on_delete=models.CASCADE, verbose_name='Tipo de Proyecto')
    T_Materia= models.ForeignKey(T_Materia, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Materia' )
    
    
  
    
    
    
    



