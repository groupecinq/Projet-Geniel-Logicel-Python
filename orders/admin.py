from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Client, Commande, LigneCommande, Invoice

admin.site.register(Client)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'statut', 'montant_total', 'date_creation', 'imprimer_facture']
    list_filter = ['statut', 'type_commande']
    search_fields = ['client__nom', 'id']
    ordering = ['-date_creation']
    
    def imprimer_facture(self, obj):
        url = reverse('generer_facture', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank" style="background-color:#f39c12; color:white; padding:5px 10px; border-radius:3px;">🖨️ Imprimer</a>', url)
    imprimer_facture.short_description = 'Facture'

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


