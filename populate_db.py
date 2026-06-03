import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Plat, Categorie
from hr.models import Employee
from orders.models import Client
from django.contrib.auth.models import User

def populate():
    print("Début de la migration des données...")
    cursor = connection.cursor()

    # 1. Catégories et Plats
    print("Migration des produits (Plats)...")
    cursor.execute("SELECT Nom, Description FROM produit")
    produits = cursor.fetchall()
    
    # Création d'une catégorie par défaut si elle n'existe pas
    cat_default, _ = Categorie.objects.get_or_create(nom="Général")
    
    for row in produits:
        nom_plat = row[0]
        description = row[1]
        if not Plat.objects.filter(nom=nom_plat).exists():
            Plat.objects.create(
                nom=nom_plat,
                description=description,
                prix=1500,  # Prix par défaut car absent de l'ancienne table
                categorie=cat_default,
                disponible=True
            )

    # 2. Clients
    print("Migration des clients...")
    cursor.execute("SELECT Nom, Prenom, Tel, Email FROM client")
    clients = cursor.fetchall()
    
    for row in clients:
        nom = f"{row[1]} {row[0]}" if row[1] else row[0]
        telephone = row[2]
        if not Client.objects.filter(nom=nom).exists():
            Client.objects.create(
                nom=nom,
                telephone=telephone,
                adresse="Non définie"
            )

    # 3. Employés
    print("Migration des employés...")
    cursor.execute("SELECT Nom, Prenom, Tel, Salaire, Date_Embauche FROM employe")
    employes = cursor.fetchall()

    for row in employes:
        nom = row[0] or "Inconnu"
        prenom = row[1] or "Inconnu"
        tel = row[2]
        salaire = row[3] or 0
        date_embauche = row[4]
        
        username = f"{prenom.lower()}_{nom.lower()}".replace(" ", "")
        
        # Création du User
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.first_name = prenom
            user.last_name = nom
            user.set_password("password123")
            user.save()
            
        if not Employee.objects.filter(user=user).exists():
            Employee.objects.create(
                user=user,
                poste="Employé Général",
                salaire_base=salaire,
                date_embauche=date_embauche if date_embauche else "2024-01-01",
                statut='Actif'
            )

    print("Migration terminée avec succès !")

if __name__ == '__main__':
    populate()
