import os

import logging.config

from dataclasses import dataclass

from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import requests
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import SQLAlchemyError

from producer import publish

logging.config.fileConfig(os.path.join('logging.conf'))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADMIN_BASE_URL'] = os.getenv('ADMIN_BASE_URL', '')

CORS(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)


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
    user_id: int
    product_id: int

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def get_all():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:product_id>/like/', methods=['POST'])
def like(product_id: int):
    admin_base_url = app.config.get('ADMIN_BASE_URL')

    if not admin_base_url:
        abort(400, 'Request URL not configured')

    try:
        response = requests.get(f'{admin_base_url}/api/user')
        data = response.json()

        product_user = ProductUser(user_id=data.get('pk'), product_id=product_id)
        db.session.add(product_user)
        db.session.commit()

        publish('product_liked', dict(pk=product_id))
    except SQLAlchemyError:
        abort(400, 'You already liked this product')
    except requests.exceptions.ConnectionError:
        abort(503, 'Failed to request a user')

    return jsonify(dict(message='success'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
