from flask import Flask, jsonify, url_for, request    
from flask_cors import CORS
app = Flask(__name__)

cors = CORS(app)




if __name__ == '__main__':
    app.run(debug=True)
