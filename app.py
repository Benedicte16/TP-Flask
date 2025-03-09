import streamlit as st
import requests

# URL de l'API
API_URL = "https://pokeapi.co/api/v2/pokemon"

# Nombre de Pokémon par page
POKEMON_PER_PAGE = 15  

# Initialisation de la session pour la pagination et le Pokémon sélectionné
if "page" not in st.session_state:
    st.session_state["page"] = 0  # Page 0 par défaut
if "selected_pokemon" not in st.session_state:
    st.session_state["selected_pokemon"] = None

# Récupération du nombre total de Pokémon
response_total = requests.get(API_URL)
if response_total.status_code == 200:
    total_pokemon = response_total.json().get("count", 0)
    total_pages = (total_pokemon // POKEMON_PER_PAGE) + (1 if total_pokemon % POKEMON_PER_PAGE else 0)
else:
    st.error("Impossible de récupérer le nombre total de Pokémon.")
    total_pokemon = 0
    total_pages = 1

current_page = st.session_state["page"]
offset = current_page * POKEMON_PER_PAGE  

# Récupération des Pokémon pour la page actuelle
response = requests.get(f"{API_URL}?offset={offset}&limit={POKEMON_PER_PAGE}")
if response.status_code == 200:
    data = response.json()
    pokemon_list = data.get("results", [])  
else:
    st.error("Erreur lors du chargement des Pokémon.")
    pokemon_list = []


# 📋 Affichage des Pokémon sous forme de grille
st.title("Trouve ton Pokémon préféré !")
cols = st.columns(5)  # 5 Pokémon par ligne
for index, pokemon in enumerate(pokemon_list):
    pokemon_name = pokemon["name"].capitalize()
    pokemon_url = pokemon["url"]

    # Récupération de l'image du Pokémon
    response_pokemon = requests.get(pokemon_url)
    if response_pokemon.status_code == 200:
        pokemon_data = response_pokemon.json()
        image_url = pokemon_data["sprites"]["front_default"]
    else:
        image_url = "https://via.placeholder.com/100"

    # Affichage du Pokémon avec un bouton cliquable
    with cols[index % 5]:
       
        st.image(image_url, width=100)
        if st.button(pokemon_name):
            st.session_state["selected_pokemon"] = pokemon_name.lower()
            st.rerun()

# 📄 Affichage du numéro de page
st.write("")
st.write(f"📄 Page {current_page + 1} / {total_pages}")
st.write("")
st.write("")

# 🔄 Boutons de navigation
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Page précédente") and current_page > 0:
        st.session_state["page"] -= 1
        st.session_state["selected_pokemon"] = None 
        st.rerun()

with col2:
    if st.button("➡️ Page suivante") and current_page < total_pages - 1:
        st.session_state["page"] += 1
        st.session_state["selected_pokemon"] = None 
        st.rerun()

# 🎯 Affichage des détails du Pokémon sélectionné
if st.session_state["selected_pokemon"]:
    pokemon_selected = st.session_state["selected_pokemon"]

    # Récupération des informations détaillées du Pokémon
    response_details = requests.get(f"{API_URL}/{pokemon_selected}")
    if response_details.status_code == 200:
        details = response_details.json()

        # Affichage des informations
        st.markdown("---")
        st.header(f"🔍 Détails de **{details['name'].capitalize()}**")
        st.image(details["sprites"]["front_default"], width=200)

        st.write(f"**📏 Taille :** {details['height']} dm")
        st.write(f"**⚖️ Poids :** {details['weight']} hg")
        st.write(f"**🌀 Types :** {', '.join([t['type']['name'] for t in details['types']])}")
    else:
        st.error("❌ Impossible de charger les détails du Pokémon.")
