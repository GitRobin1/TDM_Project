import os
from utils.download_images import download_images
from utils.process_metadata import process_metadata


def main():
    image_dir = "./images"
    metadata_file = "./export/metadata.json"
    output_metadata_file = "./export/processed_metadata.json"
    target_image_count = 100

    existing_images = len(os.listdir(image_dir)) if os.path.exists(image_dir) else 0

    if existing_images < target_image_count:
            print(f"Images manquantes...")
            download_images(image_dir=image_dir, target_image_count=target_image_count)
    else:
        print(f"Images présentes, suite du programme...")

    process_metadata(image_dir, metadata_file, output_metadata_file)
    print(f"Métadonnées mises à jour dans : {output_metadata_file}")


if __name__ == "__main__":
    main()