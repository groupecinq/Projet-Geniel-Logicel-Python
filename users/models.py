from django.db import models
from django.contrib.auth.models import User
 
class Profil(models.Model):
    ROLES = [
       ('admin',          'Administrateur'),
       ('directeur',      'Directeur'),
     ('chef_cuisinier', 'Chef Cuisinier'),
      ('cuisinier',      'Cuisinier'),
        ('serveur',        'Serveur'),
       ('stock_manager',  'Stock Manager'),
   ]
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    role       = models.CharField(max_length=20, choices=ROLES, default='serveur')
    actif      = models.BooleanField(default=True)
    telephone  = models.CharField(max_length=20, blank=True)
    photo      = models.ImageField(upload_to='profils/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.user.username} — {self.get_role_display()}'
