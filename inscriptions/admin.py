from django.contrib import admin
from .models import Membre

class MembreAdmin(admin.ModelAdmin):
    list_display = ('inscription_date_robopoly', 'title', 'first_name', 'name', 'mail', 'phone_number', 'section', 'sciper')

admin.site.register(Membre, MembreAdmin)
