from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Plat(models.Model):
    """Un plat du menu"""
    nom = models.CharField(max_length=150, verbose_name='Nom du plat')
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=8, decimal_places=2,
                               verbose_name='Prix (FCFA)')
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL,
                                   null=True, related_name='plats')
    disponible = models.BooleanField(default=True,
                                      verbose_name='Disponible ?')
    image = models.ImageField(upload_to='plats/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nom} — {self.prix} FCFA'

    class Meta:
        ordering = ['categorie', 'nom'] 

class HistoriquePrix(models.Model):
    plat             = models.ForeignKey(Plat, on_delete=models.CASCADE, related_name='historique')
    ancien_prix      = models.DecimalField(max_digits=8, decimal_places=2)
    nouveau_prix     = models.DecimalField(max_digits=8, decimal_places=2)
    date_modification = models.DateTimeField(auto_now_add=True)
    modifie_par      = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

class Recette(models.Model):
    plat = models.OneToOneField(Plat, on_delete=models.CASCADE, related_name='recette')
    temps_cuisson = models.IntegerField(help_text="Temps de cuisson en minutes")
    chef_en_charge = models.ForeignKey('hr.Employee', on_delete=models.SET_NULL, null=True, limit_choices_to={'poste__icontains': 'chef'})
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"Recette : {self.plat.nom}"

class IngredientRecette(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey('inventory.Ingredient', on_delete=models.CASCADE)
    quantite_requise = models.FloatField(help_text="Quantité requise pour un plat")

    def __str__(self):
        return f"{self.quantite_requise} {self.ingredient.unite} de {self.ingredient.nom}"
