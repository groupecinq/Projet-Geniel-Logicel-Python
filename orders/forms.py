from django import forms
from django.forms import inlineformset_factory
from .models import Commande, Client, LigneCommande

"""Formulaire pour créer/modifier un client"""
class Meta:
    model = Client
    fields = ['nom', 'numero_table', 'adresse', 'telephone']
    widgets = {
        # Personnalise l'apparence des champs HTML
        'nom': forms.TextInput(attrs={
            'class': 'form-control',     # classe Bootstrap
            'placeholder': 'Nom du client',
        }),
        'numero_table': forms.NumberInput(attrs={'class': 'form-control'}),
        'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        'telephone': forms.TextInput(attrs={'class': 'form-control'}),
    }


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = '__all__'
        widgets = {
        'client': forms.Select(attrs={'class': 'form-select'}),
        'type_commande': forms.Select(attrs={'class': 'form-select'}),
        'notes': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Instructions spéciales (allergies, préférences...)',
        }),
    }
        
LigneCommandeFormSet = inlineformset_factory(
    Commande,
    LigneCommande,
    fields=['plat', 'quantite', 'prix_unitaire'],
    extra=1,
    can_delete=True,
    widgets={
        'plat': forms.Select(attrs={'class': 'form-select'}),
        'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
    }
)        