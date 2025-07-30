from django.contrib import admin
from .models import Demande, Application, Responsable, Transfert, Audit, Satisfaction, Historique

admin.site.register(Demande)
admin.site.register(Application)
admin.site.register(Responsable)
admin.site.register(Transfert)
admin.site.register(Audit)
admin.site.register(Satisfaction)
admin.site.register(Historique)
