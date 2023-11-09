from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Restaurant, Pizza, RestaurantPizza
from app import app, db

routes_app = Blueprint('app', __name__)


@app.route('/')
def index():
    return "Welcome to the Pizza Restaurant App"

@app.route('/register-user', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({"errors": ["Validation errors"]}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"errors": ["Email already exists"]}), 400

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 201

@app.route('/register-restaurant', methods=['POST'])
def register_restaurant():
    data = request.json
    name = data.get('name')
    address = data.get('address')
    email = data.get('email')
    password = data.get('password')

    if not (name and address and email and password):
        return jsonify({"errors": ["Validation errors"]}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"errors": ["Email already exists"]}), 400

    restaurant = Restaurant(name=name, address=address, email=email, password=password)
    db.session.add(restaurant)
    db.session.commit()

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({"errors": ["Validation errors"]}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"errors": ["Invalid email or password"]}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_data = [
        {"id": restaurant.id, "name": restaurant.name, "address": restaurant.address}
        for restaurant in restaurants
    ]
    return jsonify(restaurant_data)

@app.route('/restaurant-pizzas', methods=['GET'])
def get_restaurant_pizzas():
    restaurant_pizzas = RestaurantPizza.query.all()
    restaurant_pizza_data = [
        {"id": restaurant_pizza.id, "restaurant_id": restaurant_pizza.restaurant.id,  "pizza_id": restaurant_pizza.pizza.id, "price": restaurant_pizza.price}
        for restaurant_pizza in restaurant_pizzas
    ]
    return jsonify(restaurant_pizza_data)

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_data = [
        {"id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients}
        for pizza in pizzas
    ]
    return jsonify(pizza_data)

@app.route('/restaurants', methods=['POST'])
@jwt_required()
def create_restaurant():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    data = request.json
    name = data.get('name')
    address = data.get('address')

    if not (name and address):
        return jsonify({"errors": ["Validation errors"]}), 400

    restaurant = Restaurant(name=name, address=address)
    user.restaurants.append(restaurant)

    db.session.add(restaurant)
    db.session.commit()

    return jsonify({"id": restaurant.id, "name": restaurant.name, "address": restaurant.address}), 201

@app.route('/restaurant-pizzas', methods=['POST'])
@jwt_required()
def create_restaurant_pizza():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    data = request.json
    restaurant_id = data.get('restaurant_id')
    pizza_id = data.get('pizza_id')
    price = data.get('price')

    if not (restaurant_id and pizza_id and price):
        return jsonify({"errors": ["Validation errors"]}), 400

    restaurant = Restaurant.query.get(restaurant_id)
    pizza = Pizza.query.get(pizza_id)

    if not (restaurant and pizza):
        return jsonify({"errors": ["Invalid restaurant or pizza ID"]}), 400

    restaurant_pizza = RestaurantPizza(restaurant=restaurant, pizza=pizza, price=price)
    db.session.add(restaurant_pizza)
    db.session.commit()

    return jsonify({"id": restaurant_pizza.id, "restaurant_id": restaurant_pizza.restaurant.id, "pizza_id": restaurant_pizza.pizza.id, "price": restaurant_pizza.price}), 201

@app.route('/pizzas', methods=['POST'])
@jwt_required()
def create_pizza():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    data = request.json
    name = data.get('name')
    ingredients = data.get('ingredients')

    if not (name and ingredients):
        return jsonify({"errors": ["Validation errors"]}), 400

    pizza = Pizza(name=name, ingredients=ingredients)
    user.pizzas.append(pizza)

    db.session.add(pizza)
    db.session.commit()

    return jsonify({"id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients}), 201

if __name__ == '__main__':
    app.run(debug=True)