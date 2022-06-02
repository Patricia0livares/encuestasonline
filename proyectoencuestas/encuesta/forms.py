from django import forms
from django.contrib.auth.models import User
from . import models

class ContactoForm(forms.Form):
    Nombre = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Mensaje = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

# class EncuestadorSueldoForm(forms.Form):
#     sueldo=forms.IntegerField()

class GrupoForm(forms.ModelForm):
    class Meta:
        model=models.Grupo
        fields=['grupo_name','encuesta_number','total_marks']

class EncuestaForm(forms.ModelForm):
    
    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    grupoID=forms.ModelChoiceField(queryset=models.Grupo.objects.all(),empty_label="Grupo Nombre", to_field_name="id")
    class Meta:
        model=models.Encuesta
        fields=['marks','encuesta','option1','option2','option3','option4','respuesta']
        widgets = {
            'pregunta': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
