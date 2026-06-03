from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Commande, Client, LigneCommande, Invoice
from django.http import HttpResponse
from products.models import Plat
from orders.forms import CommandeForm, LigneCommandeFormSet
from django.contrib.auth.forms import UserCreationForm

@login_required
def liste_commandes(request):
    commandes = Commande.objects.select_related('client').order_by('-date_creation')
    statut = request.GET.get('statut', '')
    if statut:
     commandes = commandes.filter(statut=statut)
    commandes = commandes.order_by('-date_creation')  
    return render(request, 'orders/liste.html', {
        'commandes': commandes, 
        'statut_filtre': statut,
    })

@login_required
def creer_commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.creee_par = request.user
            commande.save()
            messages.success(request, f'Commande #{commande.id} créée !')
            return redirect('detail_commande', pk=commande.id)
    else:
        form = CommandeForm()
    plats = Plat.objects.filter(disponible=True)  # plats disponibles pour le formulaire   
    return render(request, 'orders/creer.html', {
        'form': form
        })


@login_required
def detail_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    lignes   = commande.lignes.select_related('plat').all()
    return render(request, 'orders/detail.html', {
        'commande': commande, 
        'lignes': lignes
    })

@login_required
def changer_statut(request, pk):
    """Met à jour le statut d'une commande"""
    commande = get_object_or_404(Commande, pk=pk)

    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        commande.statut = nouveau_statut
        commande.save()
        messages.success(request, 'Statut mis à jour !')

    return redirect('detail_commande', pk=pk)

def accueil(request):
    return render(request, 'accueil.html')

from django.shortcuts import render, redirect

def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_required(request, user)
            messages.success(request, f'Bienvenue {user.username}')
            return redirect('accueil')  # après inscription, va vers la page de connexion
        else:

            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'registration/inscription.html', {'form': form})

@login_required
def generer_facture(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    invoice, created = Invoice.objects.get_or_create(commande=commande,
         defaults={'montant_ht': commande.montant_total / 1.1925,
                    'tva_pct': 19.25,
                    'montant_ttc': commande.montant_total})
      # Génération PDF via WeasyPrint
    return render(request, 'orders/facture.html', {'invoice': invoice})