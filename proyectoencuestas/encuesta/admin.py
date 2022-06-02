from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from . models import *

class EncuestaResources(resources.ModelResource):
    # fields = ('sku', 'name', 'price', 'stock')
    fields=('marks','encuesta','option1','option2','option3','option4','respuesta')
    class Meta:
        model = Encuesta

class EncuestaAdmin(ImportExportModelAdmin):
    resource_class = EncuestaResources
    
    list_display = ('marks','encuesta','option1','option2','option3','option4','respuesta')
    list_filter = ('marks','encuesta')
    search_fields = ('marks','encuesta')
    # ordering = ('-encuesta',)

admin.site.register(Encuesta,EncuestaAdmin)
