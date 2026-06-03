from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Livraisons, Coursier
from django.utils import timezone
  
@login_required
def liste_livraisons(request):
   livraisons = Livraisons.objects.select_related('commande','coursier').order_by('-date_creation')
   return render(request, 'delivery/liste.html', {'livraisons': livraisons})
   
@login_required
def affecter_coursier(request, livraison_id):
  livraisons = get_object_or_404(Livraisons, pk=livraison_id)
  if request.method == 'POST':
      coursier_id = request.POST.get('coursier')
      coursier = get_object_or_404(Coursier, pk=coursier_id)
      livraisons.coursier = coursier
      livraisons.statut = 'en_route'
      livraisons.save()
      coursier.disponible = False
      coursier.save()
      return redirect('delivery:liste')
  coursiers = Coursier.objects.filter(disponible=True)
  return render(request, 'delivery/affecter.html',
              {'livraisons': Livraisons, 'coursiers': coursiers})

