from django.db import models
from django.contrib.auth.models import User
 
class Employee(models.Model):

    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    poste          = models.CharField(max_length=100)
    salaire_base   = models.DecimalField(max_digits=10, decimal_places=2)
    prime_anciennete = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    prime_rendement = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    date_embauche  = models.DateField()
    statut         = models.CharField(max_length=20, default='actif')
    def __str__(self): return f'{self.user.get_full_name()} — {self.poste}'

class Salaire(models.Model):
    employe        = models.ForeignKey(Employee, on_delete=models.CASCADE)
    mois           = models.CharField(max_length=20)  # ex: 'avril'
    annee          = models.IntegerField()
    salaire_brut   = models.DecimalField(max_digits=10, decimal_places=2)
    cotisation_cnps = models.DecimalField(max_digits=8, decimal_places=2)
    deductions     = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    salaire_net    = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    date_versement = models.DateField(auto_now_add=True)

    def calculer_paie(self):
        self.salaire_brut = self.employe.salaire_base + self.employe.prime_anciennete + self.employe.prime_rendement
        self.salaire_net = self.salaire_brut - self.cotisation_cnps - self.deductions
        self.save()
        return self.salaire_net

class Affectation(models.Model):
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='affectations')
    role = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employe.user.get_full_name()} - {self.role}"