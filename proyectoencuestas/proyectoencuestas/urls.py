from django.urls import path,include
from django.contrib import admin
from encuesta import views 
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('encuestador/',include('encuestador.urls')),
    path('usuario/',include('usuario.urls')),
    


    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='encuesta/logout.html'),name='logout'),
    path('contacto', views.contacto_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),



    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='encuesta/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-encuestador', views.admin_encuestador_view,name='admin-encuestador'),
    path('admin-view-encuestador', views.admin_view_encuestador_view,name='admin-view-encuestador'),
    path('update-encuestador/<int:pk>', views.update_encuestador_view,name='update-encuestador'),
    path('delete-encuestador/<int:pk>', views.delete_encuestador_view,name='delete-encuestador'),
    path('admin-view-pendiente-encuestador', views.admin_view_pendiente_encuestador_view,name='admin-view-pendiente-encuestador'),
    # path('admin-view-encuestador-sueldo', views.admin_view_encuestador_sueldo_view,name='admin-view-encuestador-sueldo'),
    path('approve-encuestador/<int:pk>', views.approve_encuestador_view,name='approve-encuestador'),
    path('reject-encuestador/<int:pk>', views.reject_encuestador_view,name='reject-encuestador'),

    path('admin-usuario', views.admin_usuario_view,name='admin-usuario'),
    path('admin-view-usuario', views.admin_view_usuario_view,name='admin-view-usuario'),
    path('admin-view-usuario-marks', views.admin_view_usuario_marks_view,name='admin-view-usuario-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view,name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view,name='admin-check-marks'),
    path('update-usuario/<int:pk>', views.update_usuario_view,name='update-usuario'),
    path('delete-usuario/<int:pk>', views.delete_usuario_view,name='delete-usuario'),

    path('admin-grupo', views.admin_grupo_view,name='admin-grupo'),
    path('admin-add-grupo', views.admin_add_grupo_view,name='admin-add-grupo'),
    path('admin-view-grupo', views.admin_view_grupo_view,name='admin-view-grupo'),
    path('delete-grupo/<int:pk>', views.delete_grupo_view,name='delete-grupo'),

    path('admin-encuesta', views.admin_encuesta_view,name='admin-encuesta'),
    path('admin-add-encuesta', views.admin_add_encuesta_view,name='admin-add-encuesta'),
    path('admin-view-encuesta', views.admin_view_encuesta_view,name='admin-view-encuesta'),
    path('view-encuesta/<int:pk>', views.view_encuesta_view,name='view-encuesta'),
    path('delete-encuesta/<int:pk>', views.delete_encuesta_view,name='delete-encuesta'),


]
