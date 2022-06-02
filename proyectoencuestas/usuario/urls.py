from django.urls import path
from usuario import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('usuarioclick', views.usuarioclick_view),
path('usuariologin', LoginView.as_view(template_name='usuario/usuariologin.html'),name='usuariologin'),
path('usuariosignup', views.usuario_signup_view,name='usuariosignup'),
path('usuario-dashboard', views.usuario_dashboard_view,name='usuario-dashboard'),
path('usuario-encuesta', views.usuario_encuesta_view,name='usuario-encuesta'),
path('take-encuesta/<int:pk>', views.take_encuesta_view,name='take-encuesta'),
path('start-encuesta/<int:pk>', views.start_encuesta_view,name='start-encuesta'),

path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-resultado', views.view_resultado_view,name='view-resultado'),
path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('usuario-marks', views.usuario_marks_view,name='usuario-marks'),
]