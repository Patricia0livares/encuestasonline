from django.urls import path
from encuestador import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('encuestadorclick', views.encuestadorclick_view),
path('encuestadorlogin', LoginView.as_view(template_name='encuestador/encuestadorlogin.html'),name='encuestadorlogin'),
path('encuestadorsignup', views.encuestador_signup_view,name='encuestadorsignup'),
path('encuestador-dashboard', views.encuestador_dashboard_view,name='encuestador-dashboard'),
path('encuestador-grupo', views.encuestador_grupo_view,name='encuestador-grupo'),
path('encuestador-add-grupo', views.encuestador_add_grupo_view,name='encuestador-add-grupo'),
path('encuestador-view-grupo', views.encuestador_view_grupo_view,name='encuestador-view-grupo'),
path('delete-encuesta/<int:pk>', views.delete_encuesta_view,name='delete-encuesta'),


path('encuestador-encuesta', views.encuestador_encuesta_view,name='encuestador-encuesta'),
path('encuestador-add-encuesta', views.encuestador_add_encuesta_view,name='encuestador-add-encuesta'),
path('encuestador-view-encuesta', views.encuestador_view_encuesta_view,name='encuestador-view-encuesta'),
path('see-encuesta/<int:pk>', views.see_encuesta_view,name='see-encuesta'),
path('remove-encuesta/<int:pk>', views.remove_encuesta_view,name='remove-encuesta'),
]