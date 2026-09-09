# NovaTech

Boutique Django avec catalogue, panier, commandes et comptes utilisateurs.

## Lancer le projet

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata demo_products
python manage.py runserver
```

Ouvrez `http://127.0.0.1:8000/`. L'administration est disponible à `/admin/` pour créer des catégories et produits.

`loaddata demo_products` charge trois produits de démonstration. Le premier utilise uniquement le lien Chariow fourni ; les autres n'ont volontairement aucun lien de paiement par défaut.

Par défaut, la base SQLite est utilisée. Pour PostgreSQL, renseignez `DATABASE_URL` au format `postgresql://utilisateur:motdepasse@hote:5432/nom_base` dans `.env`.

## Fonctionnalités

- Catalogue de produits et images
- Panier conservé en session
- Commande avec décrément du stock
- Inscription, connexion et historique des commandes
- Gestion des produits et commandes dans l'administration Django

## Paiement express avec Chariow

1. Dans l'administration, ajoutez à chaque produit son **identifiant produit Chariow** et son **lien de paiement Chariow**. Pour le produit actuel, utilisez exactement `https://sbbsojae.mychariow.shop/prd_4flawwm4/checkout`.
2. Configurez une Pulse Chariow HTTPS vers `https://votre-domaine/orders/webhooks/chariow/`, pour l'événement `successful.sale`.
3. Renseignez `CHARIOW_WEBHOOK_SECRET` et `SITE_URL` dans `.env`.

Le client saisit seulement son nom et son e-mail avant la redirection. À la confirmation, NovaTech crée ou rattache automatiquement son compte et lui envoie un lien pour choisir son mot de passe, ainsi que le lien public du produit acheté. En cas de rapprochement ambigu (même e-mail et même produit avec plusieurs commandes en attente), la commande est volontairement laissée en attente : utilisez l'action « Confirmer les commandes sélectionnées comme payées » dans l'administration.

NovaTech ne fabrique ni ne modifie aucun lien Chariow : chaque produit doit avoir son propre lien renseigné manuellement dans l’administration.

## Vérifier le projet

```powershell
python manage.py test
python manage.py check
```
