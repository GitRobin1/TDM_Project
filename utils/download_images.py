import os
import json
import requests
import shutil
from SPARQLWrapper import SPARQLWrapper, JSON
from PIL import Image
from PIL.ExifTags import TAGS

def download_image(url, save_path):
    headers = {"User-Agent": "Mozilla/5.0"}
    request = requests.get(url, allow_redirects=True, headers=headers, stream=True)
    
    if request.status_code == 200:
        with open(save_path, "wb") as image:
            request.raw.decode_content = True
            shutil.copyfileobj(request.raw, image)
    
    return request.status_code

def fetch_images_from_wikidata(limit=500):
    sparql_query = f"""
    SELECT ?image WHERE {{
    ?item wdt:P31/wdt:P279* wd:Q42372;
            wdt:P18 ?image.
    FILTER (STRENDS(LCASE(STR(?image)), ".jpg") || STRENDS(LCASE(STR(?image)), ".png"))
    }} LIMIT {limit}
    """

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    sparql.addCustomHttpHeader("User-Agent", "Mozilla/5.0")


    results = sparql.query().convert()
    return [result["image"]["value"] for result in results["results"]["bindings"]]

def download_images(image_dir="./images", metadata_file="./export/metadata.json", target_image_count=100):
    os.makedirs(image_dir, exist_ok=True)
    metadata_list = []
    downloaded_images = set()
    
    while len(os.listdir(image_dir)) < target_image_count:
        print(f"🔍 Téléchargement en cours... ({len(os.listdir(image_dir))}/{target_image_count})")
        
        image_urls = fetch_images_from_wikidata(500)
        if not image_urls:
            print("⚠️ Plus d'images trouvées sur Wikidata.")
            break

        for image_url in image_urls:
            if len(os.listdir(image_dir)) >= target_image_count:
                break
            
            image_ext = os.path.splitext(image_url)[-1].lower()
            if image_url in downloaded_images:
                continue

            image_name = f"image_{len(os.listdir(image_dir)) + 1}{image_ext}"
            image_path = os.path.join(image_dir, image_name)

            try:
                status_code = download_image(image_url, image_path)
                if status_code == 200:
                    with Image.open(image_path) as img:
                        width, height = img.size
                        format = img.format
                        orientation = "Portrait" if height > width else "Paysage" if width > height else "Carré"
                        
                        exif_data = img._getexif()
                        exif_info = {TAGS.get(tag, tag): str(value) for tag, value in (exif_data or {}).items()}

                        metadata_list.append({
                            "file_name": image_name,
                            "url": image_url,
                            "width": width,
                            "height": height,
                            "format": format,
                            "orientation": orientation,
                            "exif": exif_info,
                        })
                    
                    downloaded_images.add(image_url)
                    print(f"✅ Téléchargé ({len(os.listdir(image_dir))}/{target_image_count}) : {image_name}")
                else:
                    os.remove(image_path)
                    print(f"⚠️ Échec téléchargement {image_url} - Code HTTP {status_code}")
            except Exception as e:
                if os.path.exists(image_path):
                    os.remove(image_path)
                print(f"❌ Erreur traitement {image_url} : {e}")
    
    with open(metadata_file, "w", encoding="utf-8") as json_file:
        json.dump(metadata_list, json_file, indent=4, ensure_ascii=False)

    print(f"🎉 Téléchargement terminé : {target_image_count} images enregistrées !")
    print(f"📄 Métadonnées enregistrées dans {metadata_file}")

