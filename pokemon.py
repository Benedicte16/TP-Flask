from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api/pokemon_list')
def get_pokemon_list():
    limit = 50  # Nombre de Pokémon par page
    offset = int(request.args.get("offset", 0))  # Offset pour la pagination
    
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon_list = [{"name": p["name"], "url": p["url"]} for p in data["results"]]

        # Ajouter les images de chaque Pokémon
        for p in pokemon_list:
            pokemon_data = requests.get(p["url"]).json()
            p["image"] = pokemon_data["sprites"]["front_default"]

        return jsonify(pokemon_list)
    else:
        return jsonify({"error": "Impossible de récupérer la liste des Pokémon"}), 500

if __name__ == '__main__':
    app.run(debug=True)
