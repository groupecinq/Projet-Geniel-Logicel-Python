from django.contrib import admin
from .models import Employee, Salaire, Affectation

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'poste', 'salaire_base', 'statut')
    search_fields = ('user__username', 'poste')

@admin.register(Salaire)
class SalaireAdmin(admin.ModelAdmin):
    list_display = ('employe', 'mois', 'annee', 'salaire_net')

@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ('employe', 'role', 'date_debut', 'date_fin')
