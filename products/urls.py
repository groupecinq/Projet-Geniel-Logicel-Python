from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',              views.liste_plats,  name='menu'),
    path('<int:plat_id>/',     views.detail_plat,  name='detail_plat'),
    path('menu/', views.menu, name='menu'),
    path('ajouter-au-panier/<int:plat_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.voir_panier, name='panier'),
    path('supprimer-du-panier/<int:plat_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('suivi/<int:commande_id>/', views.suivi_commande, name='suivi'),
]