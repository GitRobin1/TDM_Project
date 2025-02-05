import cv2
import numpy as np
import os
import json
from sklearn.cluster import KMeans

os.environ["LOKY_MAX_CPU_COUNT"] = "1"

def get_dominant_colors(image_path, k=5):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image introuvable : {image_path}")
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_LINEAR)
        image = image.reshape((-1, 3))
        
        kmeans = KMeans(n_clusters=k, random_state=0, n_init=5)
        kmeans.fit(image)
        
        colors = kmeans.cluster_centers_.astype(int)
        return ["#{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]) for c in colors]
    except Exception as e:
        print(f"⚠️ Erreur analyse couleur {image_path} : {e}")
        return []

def generate_tags(metadata):
    tags = set()
    if metadata.get("width") and metadata.get("height"):
        tags.add("#paysage" if metadata["width"] > metadata["height"] else "#portrait")
    if metadata.get("format"):
        tags.add(f"#{metadata['format'].lower()}")
    if "exif" in metadata and "Make" in metadata["exif"]:
        tags.add(f"#{metadata['exif']['Make'].lower()}")
    return list(tags)

def process_metadata(image_dir, metadata_file, output_file="processed_metadata.json"):
    if not os.path.isfile(metadata_file):
        print("⚠️ Fichier metadata.json introuvable.")
        return
    
    with open(metadata_file, "r", encoding="utf-8") as file:
        metadata_list = json.load(file)
    
    for metadata in metadata_list:
        image_path = os.path.join(image_dir, metadata["file_name"])
        
        try:
            metadata["colors"] = get_dominant_colors(image_path)
        except Exception as e:
            print(f"⚠️ Impossible d'extraire les couleurs pour {image_path} : {e}")
            metadata["colors"] = []

        try:
            metadata["tags"] = generate_tags(metadata)
        except Exception as e:
            print(f"⚠️ Impossible de générer les tags pour {image_path} : {e}")
            metadata["tags"] = []
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(metadata_list, file, indent=4, ensure_ascii=False)
        file.flush()
    
    print(f"✅ Métadonnées mises à jour avec les couleurs et tags. Fichier sauvegardé sous : {output_file}")

