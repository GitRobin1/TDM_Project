import streamlit as st
import os
import json
from PIL import Image

PREFERENCE_FILE = "./export/user_preferences.json"
IMAGE_DIR = "./images"
METADATA_FILE = "./export/processed_metadata.json"

def load_metadata():
    if not os.path.exists(METADATA_FILE):
        return []
    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def load_preferences():
    if os.path.exists(PREFERENCE_FILE):
        with open(PREFERENCE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_preferences(preferences):
    with open(PREFERENCE_FILE, "w", encoding="utf-8") as file:
        json.dump(preferences, file, indent=4, ensure_ascii=False)

def user_simulation():
    st.title("💖 Système de préférences utilisateur")
    
    metadata_list = load_metadata()
    if not metadata_list:
        st.error("Aucune métadonnée disponible.")
        return
    
    preferences = load_preferences()
    user_id = st.text_input("Entrez votre identifiant utilisateur :", "user_1")
    
    if user_id not in preferences:
        preferences[user_id] = {"likes": [], "dislikes": []}
    
    if "image_index" not in st.session_state:
        st.session_state.image_index = 0  # Initialisation correcte

    image_index = st.session_state.image_index
    image_metadata = metadata_list[image_index]
    image_path = os.path.join(IMAGE_DIR, image_metadata["file_name"])
    
    st.image(Image.open(image_path), caption=image_metadata["file_name"], use_container_width=True)
    st.write(f"Tags : {', '.join(image_metadata.get('tags', []))}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("❤️ Like"):
            user_pref = {
                "file_name": image_metadata["file_name"],
                "tags": image_metadata.get("tags", []),
                "colors": image_metadata.get("colors", []),
                "format": image_metadata.get("format", ""),
                "orientation": image_metadata.get("orientation", ""),
                "dimensions": f"{image_metadata.get('width', 0)}x{image_metadata.get('height', 0)}"
            }
            preferences[user_id]["likes"].append(user_pref)
            save_preferences(preferences)
            st.session_state.image_index = (image_index + 1) % len(metadata_list)
            st.rerun()
    with col3:
        if st.button("💔 Dislike"):
            user_pref = {
                "file_name": image_metadata["file_name"],
                "tags": image_metadata.get("tags", []),
                "colors": image_metadata.get("colors", []),
                "format": image_metadata.get("format", ""),
                "orientation": image_metadata.get("orientation", ""),
                "dimensions": f"{image_metadata.get('width', 0)}x{image_metadata.get('height', 0)}"
            }
            preferences[user_id]["dislikes"].append(user_pref)
            save_preferences(preferences)
            st.session_state.image_index = (image_index + 1) % len(metadata_list)
            st.rerun()
