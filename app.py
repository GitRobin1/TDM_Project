import streamlit as st
import os
import json
from PIL import Image
import matplotlib.pyplot as plt
import user_simulation 

def load_metadata(metadata_file):
    if not os.path.exists(metadata_file):
        st.error("Le fichier de métadonnées est introuvable.")
        return []
    with open(metadata_file, "r", encoding="utf-8") as file:
        return json.load(file)

def main():
    st.sidebar.title("📌 Navigation")
    page = st.sidebar.radio("Choisissez une page :", ["Visualisation des images", "Préférences utilisateur"])

    if page == "Visualisation des images":
        show_image_visualization()
    elif page == "Préférences utilisateur":
        user_simulation.user_simulation()

def show_image_visualization():
    st.title("📸 Visualisation des images et métadonnées")

    if "image_index" not in st.session_state:
        st.session_state.image_index = 0

    
    image_dir = "./images"
    metadata_file = "./export/processed_metadata.json"

    if not os.listdir(image_dir): 
        st.error("Le dossier des images est vide. L'application ne peut pas démarrer.")
        return

    metadata_list = load_metadata(metadata_file)
    if not metadata_list:
        st.warning("Aucune métadonnée disponible.")
        return

    image_files = [m["file_name"] for m in metadata_list]

    selected_image = st.selectbox("Sélectionnez une image :", image_files, key="image_select")

    image_metadata = next((m for m in metadata_list if m["file_name"] == selected_image), None)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("◁"):
            st.session_state.image_index = (st.session_state.image_index - 1) % len(image_files)
    with col3:
        if st.button("▷"):
            st.session_state.image_index = (st.session_state.image_index + 1) % len(image_files)

    selected_image = image_files[st.session_state.image_index]
    image_path = os.path.join(image_dir, selected_image)
    image = Image.open(image_path)
    image = image.resize((300, int(300 * image.height / image.width)))

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(image, caption=selected_image)

    if image_metadata:
        st.subheader("📊 Métadonnées")
        st.write(f"**Dimensions :** {image_metadata['width']}x{image_metadata['height']}")
        st.write(f"**Format :** {image_metadata['format']}")
        st.write(f"**Orientation :** {image_metadata['orientation']}")

        if "colors" in image_metadata:
            st.subheader("🎨 Couleurs dominantes")
            plot_colors(image_metadata["colors"])
            st.write(", ".join(image_metadata["colors"]))

        if "tags" in image_metadata:
            st.subheader("🏷️ Tags")
            st.write(", ".join(image_metadata["tags"]))

def plot_colors(colors):
    import matplotlib.colors as mcolors
    rgb_colors = [mcolors.to_rgb(color) if isinstance(color, str) else color for color in colors]

    fig, ax = plt.subplots(figsize=(5, 1))
    ax.imshow([rgb_colors], aspect="auto")
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)

if __name__ == "__main__":
    main()
