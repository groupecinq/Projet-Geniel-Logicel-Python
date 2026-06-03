from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee, Salaire
from decimal import Decimal
  
TAUX_CNPS = Decimal('0.042')  # 4.2% cotisation CNPS Cameroun
  
def calculer_salaire_net(employe):
   brut = employe.salaire_base + employe.prime_anciennete + employe.prime_rendement
   cnps = brut * TAUX_CNPS
   net  = brut - cnps - employe.deductions if hasattr(employe, 'deductions') else brut - cnps
   return {'brut': brut, 'cnps': cnps, 'net': net}
 
@login_required
def calculer_paies(request):
   if request.method == 'POST':
      mois  = request.POST.get('mois')
      annee = int(request.POST.get('annee'))
      employes = Employee.objects.filter(statut='actif')
      fiches   = []
      for emp in employes:
          calc = calculer_salaire_net(emp)
          s = Salaire.objects.create(
             employe=emp, mois=mois, annee=annee,
             salaire_brut=calc['brut'],
             cotisation_cnps=calc['cnps'],
             salaire_net=calc['net'])
          fiches.append(s)
      total = sum(f.salaire_net for f in fiches)
      return render(request, 'hr/rapport_paie.html',
                    {'fiches': fiches, 'total': total, 'mois': mois})
   return render(request, 'hr/calculer_paie.html')

