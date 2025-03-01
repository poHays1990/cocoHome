from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Fake database (ajoute des coordonnées pour la carte)
donnees_db = [
    {"id": "SA1222", "title": "Furnished 1BR in District 1", "price": 510, "area": 58, 
     "adresse": "Nguyen Van Nguyen St, Tan Dinh Ward, District 1", 
     "lat": 10.7889, "lng": 106.6950},  
    {"id": "SA1215", "title": "Furnished 1BR in District 10", "price": 400, "area": 40, 
     "adresse": "Ba Vi St, Ward 15, District 10", 
     "lat": 10.7763, "lng": 106.6672},  
    {"id": "SA1211", "title": "Studio in District 2", "price": 300, "area": 35, 
     "adresse": "Road 37, Binh An Ward, District 2", 
     "lat": 10.7871, "lng": 106.7290}  
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/api/apartments', methods=['GET'])
def get_apartments():
    """API qui envoie les appartements au format JSON pour Leaflet"""
    return jsonify(donnees_db)

if __name__ == '__main__':
    app.run(debug=True)



