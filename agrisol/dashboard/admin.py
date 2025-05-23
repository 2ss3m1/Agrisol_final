from django.contrib import admin
from .models import Agriculteur,Actionneur,Alerte,Plante,Capteur,Culture,Mesure,Intervalle 

# Register your models here.
admin.site.register(Agriculteur)
admin.site.register(Actionneur)
admin.site.register(Alerte)
admin.site.register(Capteur)
admin.site.register(Culture)
admin.site.register(Plante)
admin.site.register(Mesure)
admin.site.register(Intervalle)
#mdp 123456