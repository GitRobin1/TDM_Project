# Massive Data Treatment Project

Cette application permet de télécharger des images depuis Wikidata, d'extraire des métadonnées associées à ces images, d'analyser les couleurs dominantes et de générer des tags pour chaque image. L'application est ensuite visualisée dans une interface web créée avec Streamlit.

## Fonctionnalités

- **Téléchargement d'images :** Télécharge automatiquement des images depuis Wikidata.
- **Extraction des métadonnées :** Récupère les informations comme les dimensions, le format, l'orientation et les données EXIF des images.
- **Analyse des couleurs :** Extrait les couleurs dominantes des images en utilisant l'algorithme K-Means.
- **Génération de tags :** Génère des tags basés sur les métadonnées de l'image.
- **Visualisation dans Streamlit :** Affiche les images et leurs métadonnées dans une interface Streamlit interactive.

## Prérequis

Avant de lancer l'application, tu dois avoir installé Docker sur ta machine. Si tu ne l'as pas encore installé, tu peux le télécharger ici : [Docker](https://www.docker.com/products/docker-desktop).

### Dépendances

- Python 3.x
- Docker
- Les librairies Python suivantes :
  - `requests`
  - `Pillow`
  - `SPARQLWrapper`
  - `opencv-python`
  - `scikit-learn`
  - `streamlit`
  - `matplotlib`
  - `numpy`

Ces dépendances sont incluses dans le fichier `requirements.txt` et seront automatiquement installées lors de la construction de l'image Docker.

## Installation

### 1. Clone ce repository

Si tu ne l'as pas encore fait, clone ce projet dans ton répertoire local :

```bash
git clone !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cd ton-repertoire
```

### 2. Crée l'image Docker

Construis l'image Docker avec la commande suivante dans ton terminal :

```bash
docker build -t app .
```

### 3. Lance le conteneur Docker

Une fois l'image construite, exécute le conteneur :

```bash
docker run -p 8501:8501 app
```

### 4. Accède à l'application

Une fois le conteneur lancé, ouvre ton navigateur et accède à l'application en allant sur :

```
http://localhost:8501
```

Tu devrais voir l'interface Streamlit, où tu peux explorer les images téléchargées, leurs métadonnées, les couleurs dominantes et les tags.

## Structure du Projet

```
.
├── Dockerfile               # Fichier de configuration Docker
├── .dockerignore            # Fichier pour ignorer certains fichiers dans Docker
├── README.md                # Ce fichier de documentation
├── download_images.py       # Script pour télécharger les images depuis Wikidata
├── process_metadata.py      # Script pour traiter les métadonnées des images
├── main.py                  # Script principal pour lancer l'application Streamlit
├── requirements.txt         # Liste des dépendances Python
├── images/                  # Dossier contenant les images téléchargées
├── metadata.json            # Métadonnées des images téléchargées
└── processed_metadata.json  # Métadonnées traitées (avec couleurs et tags)
```

## Auteurs

- **Robin** - Créateur de ce projet
