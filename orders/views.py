from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Commande, Client, LigneCommande, Invoice
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
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


@login_required
@csrf_exempt
def checkout_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])
            type_commande = data.get('type_commande', 'sur_place')
            mode_paiement = data.get('mode_paiement', 'espece')
            
            livraison_addresse = data.get('address', '') if type_commande == 'livraison' else ''
            numero_table = data.get('table', '') if type_commande == 'sur_place' else None
            
            if not cart:
                return JsonResponse({'error': 'Le panier est vide'}, status=400)
                
            # Create or get client
            client_nom = request.user.username
            client, created = Client.objects.get_or_create(
                nom=client_nom,
                defaults={
                    'adresse': livraison_addresse,
                    'numero_table': int(numero_table) if numero_table and str(numero_table).isdigit() else None
                }
            )
            
            commande = Commande.objects.create(
                client=client,
                creee_par=request.user,
                statut='en_attente',
                type_commande=type_commande,
                mode_paiement=mode_paiement,
                livraison_addresse=livraison_addresse,
                notes=data.get('notes', '')
            )
            
            for item in cart:
                # Find plat by name since frontend uses hardcoded names
                plat = Plat.objects.filter(nom__icontains=item['name']).first()
                if not plat:
                    # If not found, skip or create a dummy one for the sake of the demo
                    continue
                    
                LigneCommande.objects.create(
                    commande=commande,
                    plat=plat,
                    quantite=item['qty'],
                    prix_unitaire=plat.prix
                )
                
            commande.calculer_total()
            
            # Generate invoice right away
            Invoice.objects.create(
                commande=commande,
                montant_ht=float(commande.montant_total) / 1.1925,
                tva_pct=19.25,
                montant_ttc=commande.montant_total
            )
            
            return JsonResponse({'success': True, 'commande_id': commande.id})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)