from django.contrib import admin
from .models import Categorie, Plat, HistoriquePrix, Recette, IngredientRecette

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)

class IngredientRecetteInline(admin.TabularInline):
    model = IngredientRecette
    extra = 1

@admin.register(Recette)
class RecetteAdmin(admin.ModelAdmin):
    list_display = ('plat', 'temps_cuisson', 'chef_en_charge')
    inlines = [IngredientRecetteInline]

@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'categorie', 'disponible')
    list_filter = ('categorie', 'disponible')
    search_fields = ('nom',)

@admin.register(HistoriquePrix)
class HistoriquePrixAdmin(admin.ModelAdmin):
    list_display = ('plat', 'ancien_prix', 'nouveau_prix', 'date_modification', 'modifie_par')
