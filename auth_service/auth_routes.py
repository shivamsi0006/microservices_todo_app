from flask import Blueprint, request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from my_database_lib import db, SECRET_KEY
from my_database_lib.models import User

auth_blueprint = Blueprint('auth', __name__)

# @auth_blueprint.route('/test', methods=['GET'])
# def home():
#     return "<p> Hello, World!</p>"

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username') 
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists!'}), 409

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({'username': user.username}, SECRET_KEY, algorithm="HS256")
    return jsonify({'token': token}), 200
