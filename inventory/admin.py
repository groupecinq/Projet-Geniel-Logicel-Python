from django.contrib import admin
from .models import Ingredient, MouvementStock, CommandeAchat, Fournisseur

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'quantite', 'unite', 'seuil_critique', 'statut')
    list_filter = ('statut',)
    search_fields = ('nom',)

@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'type_mvt', 'quantite', 'date', 'raison')
    list_filter = ('type_mvt',)
    search_fields = ('ingredient__nom',)

@admin.register(CommandeAchat)
class CommandeAchatAdmin(admin.ModelAdmin):
    list_display = ('fournisseur', 'date_commande', 'statut')

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact')
