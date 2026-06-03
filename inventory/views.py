from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ingredient, MouvementStock, CommandeAchat, Fournisseur
 
@login_required
def liste_stocks(request):
  ingredients = Ingredient.objects.all().order_by('nom')
  alertes = ingredients.filter(statut='critique')
  return render(request, 'inventory/stocks.html',
           {'ingredients': ingredients, 'alertes': alertes})
  
 
@login_required
def creer_commande_achat(request):
  if request.method == 'POST':
    fournisseur_id = request.POST.get('fournisseur')
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    commande = CommandeAchat.objects.create(fournisseur=fournisseur)
    messages.success(request, f'Commande fournisseur #{commande.id} créée !')
    return redirect('inventory:stocks')
  fournisseurs = Fournisseur.objects.all()
  return render(request, 'inventory/commande_achat.html',
               {'fournisseurs': fournisseurs})
