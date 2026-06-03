from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from .models import Plat,  Categorie , HistoriquePrix
from django.contrib import messages
  # ou le nom de ton modèle produit

def liste_produit(request):
 
    # produits = Plat.objects.all()
    # return render(request, 'products/liste.html', {'produits': produits})
    return HttpResponse("Liste des produits - À compléter")

def detail_produit(request, id):
    # produit = Plat.objects.get(id=id)
    # return render(request, 'products/detail.html', {'produit': produit})
    return HttpResponse(f"Détail du produit {id} - À compléter")

def liste_plats(request):
    """Affiche tous les plats du menu"""
    plats = Plat.objects.filter(disponible=True)  # seulement les plats disponibles
    categories = Categorie.objects.all()
    
    # Filtrer par catégorie si demandé
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        plats = plats.filter(categorie_id=categorie_id)
    
    context = {
        'plats': plats,
        'categories': categories,
        'categorie_active': int(categorie_id) if categorie_id else None,
    }
    return render(request, 'products/menu.html', context)

@login_required
def detail_plat(request, plat_id):
    """Affiche le détail d'un plat"""
    plat = Plat.objects.get(id=plat_id, disponible=True)
    return render(request, 'products/detail_plat.html', {'plat': plat})

@login_required
def modifier_plat(request, pk):
   plat = get_object_or_404(Plat, pk=pk)
   if request.method == 'POST':
    ancien_prix = plat.prix
    plat.nom = request.POST.get('nom', plat.nom)
    plat.prix = request.POST.get('prix', plat.prix)
    plat.disponible = 'disponible' in request.POST
    plat.save()
    # Enregistrer historique si prix changé
    if ancien_prix != plat.prix:
        HistoriquePrix.objects.create(
            plat=plat, ancien_prix=ancien_prix,
            nouveau_prix=plat.prix, modifie_par=request.user)
        cache.delete('catalogue_plats')  # invalider le cache
        return redirect('products:detail', pk=pk)
    return render(request, 'products/modifier.html', {'plat': plat})
   


def menu(request):
    plats = Plat.objects.filter(disponible=True)
    categories = {}
    for plat in plats:
        if plat.categorie.nom not in categories:
            categories[plat.categorie.nom] = []
        categories[plat.categorie.nom].append(plat)
    return render(request, 'products/menu.html', {'categories': categories})

def ajouter_au_panier(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id)
    panier = request.session.get('panier', {})
    if str(plat_id) in panier:
        panier[str(plat_id)]['quantite'] += 1
    else:
        panier[str(plat_id)] = {'nom': plat.nom, 'prix': str(plat.prix), 'quantite': 1}
    request.session['panier'] = panier
    messages.success(request, f"{plat.nom} ajouté au panier")
    return redirect('products:menu')

def voir_panier(request):
    panier = request.session.get('panier', {})
    total = 0
    articles = []
    for id_plat, item in panier.items():
        prix = float(item['prix'])
        quantite = item['quantite']
        sous_total = prix * quantite
        total += sous_total
        articles.append({
            'id': id_plat,
            'nom': item['nom'],
            'prix': prix,
            'quantite': quantite,
            'sous_total': sous_total
        })
    return render(request, 'products/panier.html', {'articles': articles, 'total': total})

def supprimer_du_panier(request, plat_id):
    panier = request.session.get('panier', {})
    if str(plat_id) in panier:
        del panier[str(plat_id)]
    request.session['panier'] = panier
    return redirect('products:panier')

def confirmation(request):
    if request.method == 'POST':
        # Créer la commande ici (tu peux la lier à un utilisateur connecté)
        panier = request.session.get('panier', {})
        # Simuler un ID commande
        commande_id = 123
        request.session['panier'] = {}
        return render(request, 'products/confirmation.html', {'commande_id': commande_id})
    return redirect('products:panier')

def suivi_commande(request, commande_id):
    return render(request, 'products/suivi.html', {'commande_id': commande_id})   