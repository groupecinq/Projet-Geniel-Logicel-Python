from django.contrib import admin
from .models import Client, Commande, LigneCommande, Invoice

admin.site.register(Client)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'statut', 'montant_total', 'date_creation']
    list_filter = ['statut', 'type_commande']
    search_fields = ['client__nom', 'id']
    ordering = ['-date_creation']

@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'commande', 'plat', 'quantite', 'prix_unitaire', 'sous_total']
    list_filter = ['commande__statut', 'plat']
    search_fields = ['commande__client__nom', 'commande__id']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['commande', 'montant_ht', 'tva_pct', 'montant_ttc', 'date_emission']
    list_filter = ['tva_pct']
    search_fields = ['commande__client__nom', 'commande__id']


