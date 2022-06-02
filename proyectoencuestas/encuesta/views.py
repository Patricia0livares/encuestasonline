from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from encuestador import models as EMODEL
from usuario import models as UMODEL
from encuestador import forms as EFORM
from usuario import forms as UFORM
from django.contrib.auth.models import User



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'encuesta/index.html')


def is_encuestador(user):
    return user.groups.filter(name='ENCUESTADOR').exists()

def is_usuario(user):
    return user.groups.filter(name='USUARIO').exists()

def afterlogin_view(request):
    if is_usuario(request.user):      
        return redirect('usuario/usuario-dashboard')
                
    elif is_encuestador(request.user):
        accountapproval=EMODEL.Encuestador.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('encuestador/encuestador-dashboard')
        else:
            return render(request,'encuestador/encuestador_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_usuario':UMODEL.Usuario.objects.all().count(),
    'total_encuestador':EMODEL.Encuestador.objects.all().filter(status=True).count(),
    'total_grupo':models.Grupo.objects.all().count(),
    'total_encuesta':models.Encuesta.objects.all().count(),
    }
    return render(request,'encuesta/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_encuestador_view(request):
    dict={
    'total_encuestador':EMODEL.Encuestador.objects.all().filter(status=True).count(),
    'pending_encuestador':EMODEL.Encuestador.objects.all().filter(status=False).count(),
    # 'salary':EMODEL.Encuestador.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'encuesta/admin_encuestador.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_encuestador_view(request):
    encuestadores= EMODEL.Encuestador.objects.all().filter(status=True)
    return render(request,'encuesta/admin_view_encuestador.html',{'encuestadores':encuestadores})


@login_required(login_url='adminlogin')
def update_encuestador_view(request,pk):
    encuestador=EMODEL.Encuestador.objects.get(id=pk)
    user=EMODEL.User.objects.get(id=encuestador.user_id)
    userForm=EFORM.EncuestadorUserForm(instance=user)
    encuestadorForm=EFORM.EncuestadorForm(request.FILES,instance=encuestador)
    mydict={'userForm':userForm,'encuestadorForm':encuestadorForm}
    if request.method=='POST':
        userForm=EFORM.EncuestadorUserForm(request.POST,instance=user)
        encuestadorForm=EFORM.EncuestadorForm(request.POST,request.FILES,instance=encuestador)
        if userForm.is_valid() and encuestadorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            encuestadorForm.save()
            return redirect('admin-view-encuestador')
    return render(request,'encuesta/update_encuestador.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_encuestador_view(request,pk):
    encuestador=EMODEL.Encuestador.objects.get(id=pk)
    user=User.objects.get(id=encuestador.user_id)
    user.delete()
    encuestador.delete()
    return HttpResponseRedirect('/admin-view-encuestador')




@login_required(login_url='adminlogin')
def admin_view_pendiente_encuestador_view(request):
    encuestadores= EMODEL.Encuestador.objects.all().filter(status=False)
    return render(request,'encuesta/admin_view_pendiente_encuestador.html',{'encuestadores':encuestadores})


@login_required(login_url='adminlogin')
def approve_encuestador_view(request,pk):
    encuestador=EMODEL.Encuestador.objects.get(id=pk)
    user=User.objects.get(id=encuestador.user_id)
    user.save()
    encuestador.status=True
    print(encuestador)
    encuestador.save()
    return redirect('admin-view-encuestador')  

    # COMENTE LA PARTE DEL SUELDO DEL ENCUESTADOR 
    # encuestadorSalary=forms.encuestadorSalaryForm()
    # if request.method=='POST':
    #     encuestadorSalary=forms.EncuestadorSueldoForm(request.POST)
    #     if encuestadorSalary.is_valid():
    #         encuestador=EMODEL.Encuestador.objects.get(id=pk)
    #         encuestador.sueldo=encuestadorSalary.cleaned_data['salary']
    #         encuestador.estado=True
    #         encuestador.save()
    #     else:
    #         print("form is invalid")
        # return HttpResponseRedirect('/admin-view-pendiente-encuestador')
    # return render(request,'encuesta/salary_form.html',{'encuestadorSalary':encuestadorSalary})
    #   return render(request,'encuesta/salary_form.html')

@login_required(login_url='adminlogin')
def reject_encuestador_view(request,pk):
    encuestador=EMODEL.Encuestador.objects.get(id=pk)
    user=User.objects.get(id=encuestador.user_id)
    user.delete()
    encuestador.delete()
    return HttpResponseRedirect('/admin-view-pendiente-encuestador')

# @login_required(login_url='adminlogin')
# def admin_view_encuestador_salary_view(request):
#     encuestadores= EMODEL.Encuestador.objects.all().filter(status=True)
#     return render(request,'encuesta/admin_view_encuestador_sueldo.html',{'encuestadors':encuestadores})




@login_required(login_url='adminlogin')
def admin_usuario_view(request):
    dict={
    'total_usuario':UMODEL.Usuario.objects.all().count(),
    }
    return render(request,'encuesta/admin_usuario.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_usuario_view(request):
    usuarios= UMODEL.Usuario.objects.all()
    return render(request,'encuesta/admin_view_usuario.html',{'usuario':usuarios})



@login_required(login_url='adminlogin')
def update_usuario_view(request,pk):
    usuario=UMODEL.Usuario.objects.get(id=pk)
    user=UMODEL.User.objects.get(id=usuario.user_id)
    userForm=UFORM.UsuarioUserForm(instance=user)
    usuarioForm=UFORM.UsuarioForm(request.FILES,instance=usuario)
    mydict={'userForm':userForm,'usuarioForm':usuarioForm}
    if request.method=='POST':
        userForm=UFORM.UsuarioUserForm(request.POST,instance=user)
        usuarioForm=UFORM.UsuarioForm(request.POST,request.FILES,instance=usuario)
        if userForm.is_valid() and usuarioForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            usuarioForm.save()
            return redirect('admin-view-usuario')
    return render(request,'encuesta/update_usuario.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_usuario_view(request,pk):
    usuario=UMODEL.Usuario.objects.get(id=pk)
    user=User.objects.get(id=usuario.user_id)
    user.delete()
    usuario.delete()
    return HttpResponseRedirect('/admin-view-usuario')


@login_required(login_url='adminlogin')
def admin_grupo_view(request):
    return render(request,'encuesta/admin_grupo.html')


@login_required(login_url='adminlogin')
def admin_add_grupo_view(request):
    grupoForm=forms.GrupoForm()
    if request.method=='POST':
        grupoForm=forms.GrupoForm(request.POST)
        if grupoForm.is_valid():        
            grupoForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-grupo')
    return render(request,'encuesta/admin_add_grupo.html',{'grupoForm':grupoForm})


@login_required(login_url='adminlogin')
def admin_view_grupo_view(request):
    grupos = models.Grupo.objects.all()
    return render(request,'encuesta/admin_view_grupo.html',{'grupos':grupos})

@login_required(login_url='adminlogin')
def delete_grupo_view(request,pk):
    grupo=models.Grupo.objects.get(id=pk)
    grupo.delete()
    return HttpResponseRedirect('/admin-view-grupo')



@login_required(login_url='adminlogin')
def admin_encuesta_view(request):
    return render(request,'encuesta/admin_encuesta.html')


@login_required(login_url='adminlogin')
def admin_add_encuesta_view(request):
    encuestaForm=forms.EncuestaForm()
    if request.method=='POST':
        encuestaForm=forms.EncuestaForm(request.POST)
        if encuestaForm.is_valid():
            encuesta=encuestaForm.save(commit=False)
            grupo=models.Grupo.objects.get(id=request.POST.get('grupoID'))
            encuesta.grupo=grupo
            encuesta.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-encuesta')
    return render(request,'encuesta/admin_add_encuesta.html',{'encuestaForm':encuestaForm})


@login_required(login_url='adminlogin')
def admin_view_encuesta_view(request):
    grupos= models.Grupo.objects.all()
    return render(request,'encuesta/admin_view_encuesta.html',{'grupos':grupos})

@login_required(login_url='adminlogin')
def view_encuesta_view(request,pk):
    encuestas=models.Encuesta.objects.all().filter(grupo_id=pk)
    return render(request,'encuesta/view_encuesta.html',{'encuestas':encuestas})

@login_required(login_url='adminlogin')
def delete_encuesta_view(request,pk):
    encuesta=models.Encuesta.objects.get(id=pk)
    encuesta.delete()
    return HttpResponseRedirect('/admin-view-encuesta')

@login_required(login_url='adminlogin')
def admin_view_usuario_marks_view(request):
    usuarios= UMODEL.Usuario.objects.all()
    return render(request,'encuesta/admin_view_usuario_marks.html',{'usuarios':usuarios})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    grupos = models.Grupo.objects.all()
    response =  render(request,'encuesta/admin_view_marks.html',{'grupos':grupos})
    response.set_cookie('usuario_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    grupo = models.Grupo.objects.get(id=pk)
    usuario_id = request.COOKIES.get('usuario_id')
    usuario= UMODEL.Usuario.objects.get(id=usuario_id)

    results= models.Resultado.objects.all().filter(encuesta=grupo).filter(usuario=usuario)
    return render(request,'encuesta/admin_check_marks.html',{'resultados':results})
    




def aboutus_view(request):
    return render(request,'encuesta/aboutus.html')

def contacto_view(request):
    sub = forms.ContactoForm()
    if request.method == 'POST':
        sub = forms.ContactoForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Nombre']
            message = sub.cleaned_data['Mensaje']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'encuesta/contactosuccess.html')
    return render(request, 'encuesta/contacto.html', {'form':sub})


