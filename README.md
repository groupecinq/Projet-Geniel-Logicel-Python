# Système de Gestion de Restaurant (Projet Génie Logiciel)

## 📌 Description du Projet

Ce projet est une application web complète de gestion de restaurant développée dans le cadre de notre cours d'Atelier de Génie Logiciel. L'objectif est de fournir un système centralisé et automatisé pour gérer les différentes opérations quotidiennes d'un restaurant, de la prise de commande à la gestion des stocks, en passant par les ressources humaines.

Le projet respecte une méthodologie Agile et est conçu pour être maintenu et développé par un groupe de 4 étudiants, avec une documentation technique complète et un contrôle de version strict sur GitHub.

## 🚀 Fonctionnalités (Périmètre Fonctionnel)

L'application est divisée en plusieurs modules interconnectés :

1. **🧑‍💼 Gestion des Utilisateurs (User Management)**
   - Authentification sécurisée.
   - Gestion des rôles : Administrateur, Directeur, Chef cuisinier, Cuisinier, Serveur, Stock manager.
   - Permissions spécifiques selon le rôle.

2. **🧾 Gestion des Produits et Recettes (Product & Recipe Management)**
   - Catalogue des plats (catégorisation, tarification dynamique).
   - Association plats-ingrédients (fiches techniques/recettes).
   - Temps de cuisson et quantités requises.

3. **📦 Gestion des Commandes (Order Management)**
   - Prise de commandes sur place et en livraison.
   - Calcul automatique des montants et génération de factures.

4. **🛒 Gestion des Stocks (Inventory Management)**
   - Mise à jour automatique après chaque commande.
   - Alertes de seuil critique.
   - Historique des variations et mouvements de stock.

5. **🤝 Gestion des Ressources Humaines (HR Management)**
   - Fichiers employés et affectations (planning).
   - Calcul des salaires (primes, déductions, etc.).

6. **📊 Tableau de Bord (Dashboard)**
   - Chiffre d'affaires mensuel.
   - Nombre de commandes et produits les plus vendus.
   - Suivi des dépenses d'approvisionnement.

## 🛠️ Contraintes Techniques et Architecture

Le projet est conçu autour des technologies suivantes :
- **Framework Backend** : Django (Architecture MVT respectée).
- **Langage** : Python 3.x.
- **Base de Données** : MySQL (Obligatoire).
- **ORM** : Django ORM.
- **Frontend** : HTML5, CSS3, JavaScript (Interfaces responsives, thème Premium "Dark Gold").

## ⚙️ Installation et Configuration

### Prérequis
- Python 3.8 ou supérieur
- Un serveur MySQL (ex: XAMPP, WAMP, ou MySQL Server natif)

### Étapes d'installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/votre-groupe/Projet-Geniel-Logicel-Python.git
   cd Projet-Geniel-Logicel-Python
   ```

2. **Créer et activer un environnement virtuel :**
   ```bash
   python -m venv venv
   # Sous Windows :
   venv\Scripts\activate
   # Sous Linux/Mac :
   source venv/bin/activate
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la Base de Données :**
   - Assurez-vous que votre serveur MySQL est lancé.
   - Créez une base de données nommée `Restaurant`.
   - Modifiez si besoin les accès dans `config/settings.py` (DATABASES).

5. **Appliquer les migrations :**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Lancer le serveur de développement :**
   ```bash
   python manage.py runserver
   ```
   Rendez-vous sur `http://127.0.0.1:8000/` pour voir l'application.

## 👥 Orientation et Méthodologie du Groupe

- **Agile** : Répartition des tâches sous forme de Sprints, revues de code régulières.
- **Git Flow** : Chaque fonctionnalité doit être développée sur une branche séparée avant d'être fusionnée sur la branche principale (`main`).
- **Documentation** : Le code doit être commenté et une documentation technique complète accompagne le projet.

---
*Ce projet a été réalisé avec rigueur dans le but d'allier les concepts avancés du génie logiciel à une application métier concrète.*