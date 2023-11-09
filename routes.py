from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Restaurant, Pizza, RestaurantPizza
from app import app, db

routes_app = Blueprint('app', __name__)

# Authentication and Authorization

@app.route('/register-restaurant', methods=['POST'])
def register_restaurant():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')

    # Validation checks for name, email, phone_number, and password

    existing_restaurant = Restaurant.query.filter_by(email=email).first()
    if existing_restaurant:
        return jsonify({"errors": ["Email already exists"]}), 400

    restaurant = Restaurant(name=name, email=email, phone_number=phone_number, password=password)
    db.session.add(restaurant)
    db.session.commit()

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validation checks for email and password

    restaurant = Restaurant.query.filter_by(email=email).first()

    if not restaurant or not restaurant.check_password(password):
        return jsonify({"errors": ["Invalid email or password"]}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

# Restaurant Management

@app.route('/add-pizza', methods=['POST'])
@jwt_required()
def add_pizza():
    current_user_email = get_jwt_identity()
    restaurant = Restaurant.query.filter_by(email=current_user_email).first()

    data = request.json
    name = data.get('name')
    price = data.get('price')
    image_url = data.get('image_url')

    # Validation checks for name, price, and image_url

    pizza = Pizza(name=name, price=price, image_url=image_url)
    restaurant.pizzas.append(pizza)

    db.session.add(pizza)
    db.session.commit()

    return jsonify({"id": pizza.id, "name": pizza.name, "price": pizza.price, "image_url": pizza.image_url}), 201

@app.route('/restaurant-pizzas', methods=['GET'])
@jwt_required()
def get_restaurant_pizzas():
    current_user_email = get_jwt_identity()
    restaurant = Restaurant.query.filter_by(email=current_user_email).first()

    if not restaurant:
        return jsonify({"errors": ["Restaurant not found"]}), 404

    pizzas = restaurant.pizzas
    pizza_data = [
        {"id": pizza.id, "name": pizza.name, "price": pizza.price, "image_url": pizza.image_url}
        for pizza in pizzas
    ]
    return jsonify(pizza_data)

@app.route('/edit-pizza/<int:pizza_id>', methods=['PUT'])
@jwt_required()
def edit_pizza(pizza_id):
    current_user_email = get_jwt_identity()
    restaurant = Restaurant.query.filter_by(email=current_user_email).first()

    if not restaurant:
        return jsonify({"errors": ["Restaurant not found"]}), 404

    data = request.json
    name = data.get('name')
    price = data.get('price')
    image_url = data.get('image_url')

    # Validation checks for name, price, and image_url

    pizza = Pizza.query.filter_by(id=pizza_id, restaurant_id=restaurant.id).first()

    if not pizza:
        return jsonify({"errors": ["Pizza not found"]}), 404

    pizza.name = name
    pizza.price = price
    pizza.image_url = image_url

    db.session.commit()

    return jsonify({"id": pizza.id, "name": pizza.name, "price": pizza.price, "image_url": pizza.image_url}), 200
