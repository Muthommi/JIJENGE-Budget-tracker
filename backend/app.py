#!/usr/bin/python3

from flask import Flask
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_routes
from routes.transaction_routes import transaction_routes
from routes.summary_routes import summary_routes

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

# Blueprints
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(transaction_routes, url_prefix='/api')
app.register_blueprint(summary_routes, url_prefix='/api')

@app.route('/')
def home():
    return "Hello, Flask!"


if __name__ == '__main__':
    app.run(debug=True)
