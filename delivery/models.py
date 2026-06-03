from django.db import models
from django.conf import settings

import orders

class Coursier(models.Model):
   nom        = models.CharField(max_length=100)
   telephone  = models.CharField(max_length=20)
   disponible = models.BooleanField(default=True)
   def __str__(self): return f'{self.nom} — {"Dispo" if self.disponible else "Occupé"}'
 
class Livraison(models.Model):
   STATUTS = [('en_attente','En attente'),('en_route','En route'),
              ('livree','Livrée'),('annulee','Annulée')]
   commande        = models.ForeignKey('orders.Commande', on_delete=models.CASCADE)
   coursier        = models.ForeignKey(Coursier, on_delete=models.SET_NULL, null=True)
   adresse_livraison = models.TextField()
   statut          = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
   date_creation   = models.DateTimeField(auto_now_add=True)
   date_livraison  = models.DateTimeField(null=True, blank=True)
   def __str__(self): return f'Livraison #{self.id} — {self.statut}'


