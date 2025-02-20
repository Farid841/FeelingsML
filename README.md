# FeelingsML API avec Flask

Ce projet est une API Flask permettant d'analyser les sentiments d'une liste de tweets. Elle attribue un score de sentiment pour chaque tweet et stocke les résultats dans une base de données MySQL.

## Fonctionnalités

- **Analyse des sentiments** : Un endpoint `POST /analyze` qui accepte une liste de tweets et retourne un score de sentiment pour chaque tweet.
- **Stockage des données** : Les tweets analysés sont enregistrés dans une base de données MySQL.
- **Test de l'API** : Un endpoint `GET /ping` pour vérifier que l'API est opérationnelle.

## Prérequis

- **Python >= 3.9** : Assurez-vous d'avoir installé Python 3.12 ou une version plus récente.
- **Docker** : Utilisé pour exécuter l'application et la base de données MySQL dans des conteneurs.

## Installation

### 1. Configurer l'environnement virtuel

Créez un environnement virtuel Python et activez-le :

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # Sur Linux/Mac
.\.venv\Scripts\activate  # Sur Windows
```

### 2. Installer les dépendances

Installez les dépendances Python nécessaires :

```bash
pip install -r requirements.txt
```

### 3. Configurer la base de données

#### a) Sans Docker

Si vous avez déjà un service MySQL en cours d'exécution sur `localhost`, aucune modification n'est nécessaire. Flask-Migrate s'occupera de la création et de la migration des tables. Si la base de données n'existe pas encore, vous pouvez utiliser le fichier `init.sql` pour la créer avant d'exécuter les migrations.

Si vos identifiants de connexion MySQL ne sont pas les mêmes que ceux définis par défaut, modifiez-les dans le fichier `_init_.py` du dossier `app` pour assurer une bonne connexion à la base de données.

#### b) Avec Docker

Si vous souhaitez exécuter un conteneur MySQL avec Docker, utilisez la commande suivante :

```bash
docker-compose up -d db
```

Cela va :
- Démarrer un conteneur MySQL avec les configurations définies dans `docker-compose.yml`.
- Assurer que la base de données est prête avant d'exécuter les migrations.

### 4. Lancer l'application Flask

Lancez l'application Flask avec les commandes suivantes :

```bash
export FLASK_APP=app # on linux
$env:FLASK_APP="app" # on windows (beurk)
flask db upgrade
flask run
```

L'API sera accessible à l'adresse suivante :

```
http://localhost:5000
```

### 5. Lancer l'application avec Docker Compose

Assurez-vous que Docker est installé et en cours d'exécution sur votre machine.

Utilisez Docker Compose pour démarrer l'application Flask et la base de données MySQL :

```bash
docker-compose up --build
```

Cela va :

- Construire l'image Docker pour l'application Flask.
- Lancer un conteneur MySQL.
- Exécuter l'application Flask.

## Utilisation de l'API

### Endpoints disponibles

L'API propose les endpoints suivants :

- **`GET /ping`** : Vérifie que l'API est en ligne.
- **`POST /analyze`** : Analyse le sentiment d'une liste de tweets et retourne les résultats.
- **`GET /api/docs`** : Accède à la documentation interactive Swagger de l'API.


### Vérifier si l'API est opérationnelle

Effectuez une requête `GET` sur l'endpoint `/ping` :

```bash
curl -X GET http://localhost:5000/ping
```

Réponse attendue :

```json
{"status": "ok"}
```

=> fichier `reflexion` qui montre l'efort de reflexion qu'il ya eu derriere
