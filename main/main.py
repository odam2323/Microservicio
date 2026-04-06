from dataclasses import dataclass
from os import abort
from urllib import request

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # <--- CAMBIO 1: Importación necesaria
from sqlalchemy import UniqueConstraint
import requests

from producer import publish

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db:3306/main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db) # <--- CAMBIO 2: Inicialización necesaria

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    
    # CAMBIO 3: La restricción debe estar en __table_args__
    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='user_product_unique'),)


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    # Usa requests con la URL entre comillas
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    try:
        
        product_user = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()
        
        publish('product_liked', id)
        
    except:
        abort(400, 'You already liked this product')
    
    return jsonify(
        
        {
            'message': 'success'
        }
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



