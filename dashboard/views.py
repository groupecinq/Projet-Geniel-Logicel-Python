from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count, Sum
from orders.models import Commande, LigneCommande
from inventory.models import Ingredient
from hr.models import Salaire
from datetime import date
  
@login_required
def accueil(request):
  mois  = request.GET.get('mois', date.today().month)
  annee = request.GET.get('annee', date.today().year)
  cache_key = f'dashboard_{mois}_{annee}'

  data = cache.get(cache_key)
  if not data:
        # KPI 1 — Chiffre d'affaires et commandes
       agg = Commande.objects.filter(
          date_creation__month=mois,
          date_creation__year=annee
         ).aggregate(nb=Count('id'), ca=Sum('montant_total'))

        # KPI 2 — Top 5 plats
       top_plats = LigneCommande.objects.filter(
          commande__date_creation__month=mois
        ).values('plat__nom').annotate(total=Sum('quantite')).order_by('-total')[:5]

       # KPI 3 — Stocks critiques
       stocks_critiques = Ingredient.objects.filter(statut='critique').count()
 
      # KPI 4 — Masse salariale
       masse = Salaire.objects.filter(mois=mois, annee=annee).aggregate(s=Sum('salaire_net'))['s'] or 0
 
       data = {'nb_commandes': agg['nb'], 'ca': agg['ca'] or 0,
                'top_plats': list(top_plats), 'stocks_critiques': stocks_critiques,
                'masse_salariale': masse}
       cache.set(cache_key, data, timeout=300)  # cache 5 minutes

       return render(request, 'dashboard/accueil.html', {**data, 'mois': mois, 'annee': annee})

