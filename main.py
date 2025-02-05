import os
from download_images import download_images
from process_metadata import process_metadata
import time


def main():
    image_dir = "./images"
    metadata_file = "./metadata.json"
    output_metadata_file = "./processed_metadata.json"
    target_image_count = 100

    existing_images = len(os.listdir(image_dir)) if os.path.exists(image_dir) else 0

    if existing_images < target_image_count:
        print("ðŸ“¥ TÃ©lÃ©chargement des images manquantes...")
        download_images(image_dir=image_dir, target_image_count=target_image_count)
    else:
        print("âœ… Toutes les images sont dÃ©jÃ  tÃ©lÃ©chargÃ©es. Suite du programme...")

    process_metadata(image_dir, metadata_file, output_metadata_file)
    print(f"ðŸŽ¯ MÃ©tadonnÃ©es mises Ã  jour dans : {output_metadata_file}")


    while True:
        print("Mon programme s'exécute toujours...")
        time.sleep(10)

if __name__ == "__main__":
    main()