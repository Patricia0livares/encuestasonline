from django.db import models

from usuario.models import Usuario

class Grupo(models.Model):
   grupo_name = models.CharField(max_length=50)
   encuesta_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   def __str__(self):
        return self.grupo_name

class Encuesta(models.Model):
    grupo=models.ForeignKey(Grupo,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    encuesta=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    respuesta=models.CharField(max_length=200,choices=cat)

class Resultado(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    encuesta = models.ForeignKey(Grupo,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

