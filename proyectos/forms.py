from django import forms
from .models import T_Proyectos
from .models import T_Fase_proyecto
from .models import T_Gestion
from .models import T_Materia
from .models import T_Semestre
from .models import T_Tipo_Proyecto
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PForm(forms.ModelForm):
    class Meta:
        model = T_Proyectos
        fields = ['Titulo','Fecha_Inicio','Fecha_Finalizacion','Descripcion','Documentacion','Imagen','T_Fase_proyecto','T_Gestion',
                   'T_Tipo_Proyecto','T_Materia']
      
    Fecha_Inicio = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    Fecha_Finalizacion = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    Descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la Descripcion'}))
    
    
    
# 'descripcion_Problema': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Ingrese la Descripcion' }),
    # ['Titulo','Fecha_Inicio','Fecha_Finalizacion','Descripcion','Documentacion','Imagen','T_Fase_proyecto','T_Gestion',
             #      'T_Tipo_Proyecto','T_Materia']

class FForm(forms.ModelForm):
    class Meta:
        model = T_Fase_proyecto
        fields = '__all__'
        
class GForm(forms.ModelForm):
    class Meta:
        model = T_Gestion
        fields = '__all__'

class MForm(forms.ModelForm):
    class Meta:
        model = T_Materia
        
        fields = '__all__'
    


class SForm(forms.ModelForm):
    class Meta:
        model = T_Semestre
        fields = '__all__'
        
class TForm(forms.ModelForm):
    class Meta:
        model = T_Tipo_Proyecto
        fields = '__all__'
        
        
#permisos usuarios
class SuperuserPermissionForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega cualquier personalización adicional aquí si es necesario
        
class RegistrationForm(UserCreationForm):
    # Agrega campos adicionales si es necesario
    is_superuser = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = self.cleaned_data['is_superuser']
        user.is_staff = self.cleaned_data['is_staff']
        user.is_active = self.cleaned_data['is_active']
        if commit:
            user.save()
        return user