from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    nom            = models.CharField(max_length=100)
    adresse        = models.TextField(blank=True)
    numero_table   = models.IntegerField(null=True, blank=True)
    telephone      = models.CharField(max_length=20, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Client {self.nom} — Table {self.numero_table}'


class Commande(models.Model):
    STATUTS = [('en_attente','En attente'), ('en_preparation','En préparation'),
               ('pret','Prêt'), ('livre','Livré'), ('annule','Annulé')]
    TYPES   = [('sur_place','Sur place'), ('livraison','Livraison'), ('emporter', 'À emporter')]
    MODE_PAIEMENT = [('espece', 'Espèce'), ('carte', 'Carte Bancaire'), ('momo', 'MTN Mobile Money'), ('orange', 'Orange Money')]

    client         = models.ForeignKey(Client, on_delete=models.CASCADE,
                                       related_name='commandes')
    creee_par      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    statut         = models.CharField(max_length=50, choices=STATUTS,
                                      default='en_attente')
    type_commande  = models.CharField(max_length=20, choices=TYPES,
                                      default='sur_place')
    mode_paiement  = models.CharField(max_length=20, choices=MODE_PAIEMENT,
                                      default='espece')
    date_creation  = models.DateTimeField(auto_now_add=True)
    montant_total  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes          = models.TextField(blank=True)
    livraison_addresse = models.TextField(blank=True, null=True)

    def calculer_total(self):
        total = sum(item.sous_total() for item in self.lignes.all())
        self.montant_total = total
        self.save()
        return total

    def __str__(self):
        return f'Commande #{self.id} — {self.client.nom} — {self.statut}'


class LigneCommande(models.Model):
    commande      = models.ForeignKey(Commande, on_delete=models.CASCADE,
                                      related_name='lignes')
    plat          = models.ForeignKey('products.Plat', on_delete=models.PROTECT)
    quantite      = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=8, decimal_places=2)

    def sous_total(self):
        return self.quantite * self.prix_unitaire
    def __str__(self):
        return f'{self.quantite}x{self.plat.nom}'

class Invoice(models.Model):
      commande    = models.OneToOneField(Commande, on_delete=models.CASCADE)
      montant_ht  = models.DecimalField(max_digits=10, decimal_places=2)
      tva_pct     = models.FloatField(default=19.25)
      montant_ttc = models.DecimalField(max_digits=10, decimal_places=2)
      date_emission = models.DateTimeField(auto_now_add=True)
      pdf_path    = models.CharField(max_length=255, blank=True)