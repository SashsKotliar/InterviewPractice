import requests
import csv

from flask import Flask, jsonify

app = Flask(__name__)

def fetch_alive_earth_humans():
    url = "https://rickandmortyapi.com/api/character"
    params = {
        "status": "alive",
        "species": "human"
    }

    earth_humans = []

    print("Fetching data from Rick and Morty API...")

    while url:
        response = requests.get(url, params)

        if response.status_code != 200:
            break

        data = response.json()

        for char in data.get('results', []):
            origin = char.get('origin', {}).get('name', '').lower()
            if 'earth' in origin:
                character_data = {
                    'name': char.get('name'),
                    'location': char.get('location', {}).get('name'),
                    'image-url': char.get('image')
                }
                earth_humans.append(character_data)

        url = data.get('info', {}).get('next')
        params = None

    csv_filename = "alive-earth-humans.csv"
    print(f"Found {len(earth_humans)} alive human characters from Earth...")

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['name', 'location', 'image-url']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(earth_humans)

    print("File was succeessfully updated")  

    return earth_humans

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy", "message": "API is running"}), 200

@app.route('/api/characters/earth-humans', methods=['GET'])
def get_alive_earth_humans():
    data = fetch_alive_earth_humans()
    return jsonify({
        "count": len(data),
        "results": data,
    }), 200

if __name__ == "__main__":
    fetch_alive_earth_humans()
    app.run(debug=True, host='0.0.0.0', port=5000)
    