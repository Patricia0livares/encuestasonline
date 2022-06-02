from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from encuesta import models as QMODEL
from encuestador import models as TMODEL


#for showing signup/login button for usuario
def usuarioclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'usuario/usuarioclick.html')

def usuario_signup_view(request):
    userForm=forms.UsuarioUserForm()
    usuarioForm=forms.UsuarioForm()
    mydict={'userForm':userForm,'usuarioForm':usuarioForm}
    if request.method=='POST':
        userForm=forms.UsuarioUserForm(request.POST)
        usuarioForm=forms.UsuarioForm(request.POST,request.FILES)
        if userForm.is_valid() and usuarioForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            usuario=usuarioForm.save(commit=False)
            usuario.user=user
            usuario.save()
            my_usuario_group = Group.objects.get_or_create(name='USUARIO')
            my_usuario_group[0].user_set.add(user)
        return HttpResponseRedirect('usuariologin')
    return render(request,'usuario/usuariosignup.html',context=mydict)

def is_usuario(user):
    return user.groups.filter(name='USUARIO').exists()

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def usuario_dashboard_view(request):
    dict={
    
    'total_grupo':QMODEL.Grupo.objects.all().count(),
    'total_encuesta':QMODEL.Encuesta.objects.all().count(),
    }
    return render(request,'usuario/usuario_dashboard.html',context=dict)

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def usuario_encuesta_view(request):
    grupos=QMODEL.Grupo.objects.all()
    return render(request,'usuario/usuario_encuesta.html',{'grupos':grupos})

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def take_encuesta_view(request,pk):
    grupo=QMODEL.Grupo.objects.get(id=pk)
    total_questions=QMODEL.Encuesta.objects.all().filter(grupo=grupo).count()
    questions=QMODEL.Encuesta.objects.all().filter(grupo=grupo)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'usuario/take_encuesta.html',{'grupo':grupo,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def start_encuesta_view(request,pk):
    grupo=QMODEL.Grupo.objects.get(id=pk)
    questions=QMODEL.Encuesta.objects.all().filter(grupo=grupo)
    if request.method=='POST':
        pass
    response= render(request,'usuario/start_encuesta.html',{'grupo':grupo,'questions':questions})
    response.set_cookie('grupo_id',grupo.id)
    return response


@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def calculate_marks_view(request):
    if request.COOKIES.get('grupo_id') is not None:
        grupo_id = request.COOKIES.get('grupo_id')
        grupo=QMODEL.Grupo.objects.get(id=grupo_id)
        
        total_marks=0
        encuesta=QMODEL.Encuesta.objects.all().filter(grupo=grupo)
        for i in range(len(encuesta)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = encuesta[i].respuesta
            if selected_ans == actual_answer:
                total_marks = total_marks + encuesta[i].marks
        usuario = models.Usuario.objects.get(user_id=request.user.id)
        resultado = QMODEL.Resultado()
        resultado.marks=total_marks
        resultado.encuesta=grupo
        resultado.usuario=usuario
        resultado.save()

        return HttpResponseRedirect('view-resultado')



@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def view_resultado_view(request):
    grupos=QMODEL.Grupo.objects.all()
    return render(request,'usuario/view_resultado.html',{'grupos':grupos})
    

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def check_marks_view(request,pk):
    grupo=QMODEL.Grupo.objects.get(id=pk)
    usuario = models.Usuario.objects.get(user_id=request.user.id)
    resultados= QMODEL.Resultado.objects.all().filter(encuesta=grupo).filter(usuario=usuario)
    return render(request,'usuario/check_marks.html',{'resultados':resultados})

@login_required(login_url='usuariologin')
@user_passes_test(is_usuario)
def usuario_marks_view(request):
    grupos=QMODEL.Grupo.objects.all()
    return render(request,'usuario/usuario_marks.html',{'grupos':grupos})
  