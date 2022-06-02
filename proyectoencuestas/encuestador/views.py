from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from encuesta import models as QMODEL
from usuario import models as UMODEL
from encuesta import forms as QFORM


#for showing signup/login button for encuestador
def encuestadorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'encuestador/encuestadorclick.html')

def encuestador_signup_view(request):
    userForm=forms.EncuestadorUserForm()
    encuestadorForm=forms.EncuestadorForm()
    mydict={'userForm':userForm,'encuestadorForm':encuestadorForm}
    
    if request.method=='POST':
        userForm=forms.EncuestadorUserForm(request.POST)
        encuestadorForm=forms.EncuestadorForm(request.POST,request.FILES)
        if userForm.is_valid() and encuestadorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            encuestador=encuestadorForm.save(commit=False)
            encuestador.user=user
            print(encuestador)
            encuestador.save()
            my_encuestador_group = Group.objects.get_or_create(name='ENCUESTADOR')
            my_encuestador_group[0].user_set.add(user)
        return HttpResponseRedirect('encuestadorlogin')
    return render(request,'encuestador/encuestadorsignup.html',context=mydict)



def is_encuestador(user):
    return user.groups.filter(name='ENCUESTADOR').exists()

@login_required(login_url='encuestadorlogin')
@user_passes_test(is_encuestador)
def encuestador_dashboard_view(request):
    dict={    
    'total_grupo':QMODEL.Grupo.objects.all().count(),
    'total_encuesta':QMODEL.Encuesta.objects.all().count(),
    'total_usuario':UMODEL.Usuario.objects.all().count()
    }
    return render(request,'encuestador/encuestador_dashboard.html',context=dict)

@login_required(login_url='encuestadorlogin')
@user_passes_test(is_encuestador)
def encuestador_grupo_view(request):
    return render(request,'encuestador/encuestador_grupo.html')


@login_required(login_url='encuestadorlogin')
@user_passes_test(is_encuestador)
def encuestador_add_grupo_view(request):
    grupoForm=QFORM.GrupoForm()
    if request.method=='POST':
        grupoForm=QFORM.GrupoForm(request.POST)
        if grupoForm.is_valid():        
            grupoForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/encuestador/encuestador-view-encuesta')
    return render(request,'encuestador/encuestador_add_grupo.html',{'grupoForm':grupoForm})

@login_required(login_url='encuestadorlogin')
@user_passes_test(is_encuestador)
def encuestador_view_grupo_view(request):
    grupos = QMODEL.Grupo.objects.all()
    return render(request,'encuestador/encuestador_view_grupo.html',{'grupos':grupos})

@login_required(login_url='encuestadorlogin')
@user_passes_test(is_encuestador)
def delete_encuesta_view(request,pk):
    grupo=QMODEL.Grupo.objects.get(id=pk)
    grupo.delete()
    return HttpResponseRedirect('/encuestador/encuestador-view-encuesta')

@login_required(login_url='adminlogin')
def encuestador_encuesta_view(request):
    return render(request,'encuestador/encuestador_encuesta.html')

@login_required(login_url='encuestadorlogin')
@user_passes_test(is_encuestador)
def encuestador_add_encuesta_view(request):
    encuestaForm=QFORM.EncuestaForm()
    if request.method=='POST':
        encuestaForm=QFORM.EncuestaForm(request.POST)
        if encuestaForm.is_valid():
            encuesta=encuestaForm.save(commit=False)
            grupo=QMODEL.Grupo.objects.get(id=request.POST.get('grupoID'))
            encuesta.grupo=grupo
            encuesta.save()       
        else:
            print("El formulario no es valido")
        return HttpResponseRedirect('/encuestador/encuestador-view-encuesta')
    return render(request,'encuestador/encuestador_add_encuesta.html',{'encuestaForm':encuestaForm})

@login_required(login_url='encuestadorlogin')
@user_passes_test(is_encuestador)
def encuestador_view_encuesta_view(request):
    grupos= QMODEL.Grupo.objects.all()
    return render(request,'encuestador/encuestador_view_encuesta.html',{'grupos':grupos})

@login_required(login_url='encuestadorlogin')
@user_passes_test(is_encuestador)
def see_encuesta_view(request,pk):
    encuestas=QMODEL.Encuesta.objects.all().filter(grupo_id=pk)
    return render(request,'encuestador/see_encuesta.html',{'encuestas':encuestas})

@login_required(login_url='encuestadorlogin')
@user_passes_test(is_encuestador)
def remove_encuesta_view(request,pk):
    encuesta=QMODEL.Encuesta.objects.get(id=pk)
    encuesta.delete()
    return HttpResponseRedirect('/encuestador/encuestador-view-encuesta')
