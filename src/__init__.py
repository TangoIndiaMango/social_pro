from flask import Flask, jsonify, redirect
import os
from src.auth import auth
from src.post import post
from src.database import db, Post
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import sys


def create_app(test_config=None):

    app = Flask(__name__,
    instance_relative_config=True)

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY= os.environ.get('JWT_SECRET_KEY'),   

            CORS_HEADERS= "Content-Type"
        )


            
    else:
         app.config.from_mapping(test_config)  


    db.app = app
    db.init_app(app)
#based on secret_key decrypt and encrypt .flaskenv file for more info
    JWTManager(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(post)

    CORS(app)
        # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response


#to keep track of the visits on link. we take the shorturl since thats what the user will be visiting.

    
    @app.route('/')
    def hello():
        return 'Hello World!'
 



    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Server error'
        }), 500


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400




    return app
