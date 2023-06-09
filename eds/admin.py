from django.contrib import admin
from .models import Companias, Surtidores, Registroseriales, Cierreseriales, Tanques, RegistroTanques, MedidasTanques, Aplicaciones
# Register your models here.

admin.site.register(Companias)
admin.site.register(Surtidores)
admin.site.register(Registroseriales)
admin.site.register(Cierreseriales)
admin.site.register(Tanques)
admin.site.register(RegistroTanques)
admin.site.register(MedidasTanques)
admin.site.register(Aplicaciones)


