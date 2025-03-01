from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, LoginManager

from werkzeug import generate_password_hash, check_password_hash


login = LoginManager()
db = SQLAlchemy()

# Example Model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    pw_hash = db.Column(db.String())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)




from flask import Flask, render_template
from flask import request

app = Flask(__name__)

donnees_db = [
    {"id": "SA1222", "title": "Furnished Dist 1 1 bedroom apartment for rent near central area | SA1222", "price": 510, "area": 58, "adresse": "Nguyen Van Nguyen St, Tan Dinh Ward, District 1", "utilities": ["air-conditioner", "cable tv", "cafeteria", "cleaning", "convenient store", "fridge", "internet", "parking", "pets allow", "restaurant", "school", "tv", "washing machine", "wi-fi", "window"]},
    {"id": "SA1215", "title": "Furnished District 10 apartment for rent in Ho Chi Minh City | SA1215", "price": 400, "area": 40, "adresse": "Ba Vi St, Ward 15, District 10", "utilities": ["air-conditioner", "balcony", "basement", "cable tv", "cafeteria", "cleaning", "convenient store", "elevator", "fridge", "internet", "parking", "restaurant", "tv", "washing machine", "wi-fi", "window"]},
    {"id": "SA1211", "title": "Serviced studio apartment for rent in District 2 Ho Chi Minh City | SA1211", "price": 300, "area": 35, "adresse": "Road 37, Binh An Ward, District 2", "utilities": ["air-conditioner", "balcony", "cable tv", "cafeteria", "cleaning", "convenient store", "fridge", "green space", "internet", "parking", "restaurant", "tv", "washing machine", "wi-fi", "window"]},
 ]


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/map')
def map():
    price = request.args.get('price')  # Récupère le prix depuis l'URL
    if price:
        try:
            price = int(price)  # Convertir en int pour comparaison
            entites_selectionnees = [entite for entite in donnees_db if entite['price'] == price]
        except ValueError:
            entites_selectionnees = []  # Si conversion échoue, retourne une liste vide
    else:
        entites_selectionnees = []  # Si aucun prix fourni, afficher rien

    return render_template('map.html', entites_selectionnees=entites_selectionnees)


if __name__ == '__main__':
    app.run(debug=True)