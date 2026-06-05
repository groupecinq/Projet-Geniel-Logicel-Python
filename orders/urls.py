from django.urls import path
from . import views

urlpatterns = [
    path('',              views.liste_commandes,  name='liste_commandes'),
    path('nouvelle/',     views.creer_commande,   name='creer_commande'),
    path('<int:pk>/',     views.detail_commande,  name='detail_commande'),
    path('<int:pk>/statut/', views.changer_statut, name='changer_statut'),
    path('api/checkout/', views.checkout_api, name='checkout_api'),
    path('<int:pk>/facture/', views.generer_facture, name='generer_facture'),
]
