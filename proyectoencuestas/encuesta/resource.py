from import_export import resources
from .models import Encuesta

class EncuestaResource(resources.ModelResource):
    class Meta:
        model = Encuesta