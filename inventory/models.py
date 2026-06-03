from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
  
class Ingredient(models.Model):
   nom             = models.CharField(max_length=100)
   unite           = models.CharField(max_length=20)  # kg, L, pièce
   quantite        = models.FloatField(default=0)
   seuil_critique  = models.FloatField(default=1)
   statut          = models.CharField(max_length=20, default='normal')
   def __str__(self): return f'{self.nom} ({self.quantite} {self.unite})'
 

class MouvementStock(models.Model):
    TYPES = [('entree','Entrée'),('sortie','Sortie'),('ajustement','Ajustement')]
    ingredient  = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    type_mvt    = models.CharField(max_length=20, choices=TYPES)
    quantite    = models.FloatField()
    date        = models.DateTimeField(auto_now_add=True)
    raison      = models.TextField(blank=True)
    
class CommandeAchat(models.Model):
    fournisseur    = models.ForeignKey('Fournisseur', on_delete=models.PROTECT)
    date_commande  = models.DateTimeField(auto_now_add=True)
    statut      = models.CharField(max_length=20, default='en_attente')
  
class Fournisseur(models.Model):
    nom     = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    adresse = models.TextField(blank=True)
  
 # Signal automatique — déclenché quand un ingrédient est sauvegardé
@receiver(post_save, sender=Ingredient)
def verifier_seuil_critique(sender, instance, **kwargs):
  if instance.quantite <= instance.seuil_critique:
    instance.statut = 'critique'
    Ingredient.objects.filter(pk=instance.pk).update(statut='critique')