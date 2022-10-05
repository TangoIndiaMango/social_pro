from os import access
from flask import Blueprint, request, jsonify
from sqlalchemy import Identity
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from src.database import User, db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import sys



auth= Blueprint("auth",__name__,url_prefix="/api/v1/auth" )

# register user
@auth.post('/register')
def register():
    username= request.json['username']
    email= request.json['email']
    profilePic = request.json['profilePic']
    password= request.json['password']

    if len(password) < 6:
        return jsonify({
            'error': 'password is too short'
        }), 400

    if len(username) < 3:
        return jsonify({
            'error': 'Username is too short'
        }), 400

    if not username.isalnum or " " in username:
        return jsonify({
            'error': 'Username should be alphanumeric, also no spaces'
        }), 400

# using validators to validate email pip install validators
    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), 409
#if email exists
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'Email exists'}), 409

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username exists'}), 409

# hashing the password
    pwd_hash = generate_password_hash(password)

    try:
        data = User(username=username, profilePic=profilePic, password=pwd_hash, email=email)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'message': 'user created',
            'user':{
                'username': username,
                'email': email
        }}), 200
    except:

        error = True
        db.session.rollback()
        print(sys.exc_info())


@auth.post('/login')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')


    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({

                'user':{
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email,
                    }
            }), 201
    return jsonify({'error': 'Wrong credentials'}), 401   




#get user also jwt_required gives access to the user / protect endpoint
@auth.get('/me')
@jwt_required()
def me():
# to get the user identity
    user_id = get_jwt_identity()
    user = User.query.filter_by(id =user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email,
    }), 200

# for the refresh route we'll need the user to provide us with the refresh token, can use a get. Dose't mean
@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access= create_access_token(identity=identity)

    return jsonify({
        'access': access,
    }), 200