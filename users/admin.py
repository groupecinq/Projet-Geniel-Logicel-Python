from django.contrib import admin
from .models import Profil

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'actif', 'telephone')
    list_filter = ('role', 'actif')
    search_fields = ('user__username',)
