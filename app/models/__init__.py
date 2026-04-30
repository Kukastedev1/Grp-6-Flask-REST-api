from flask import Flask

def create_app():
    app = Flask(__name__)

    # config stuff...

    app.register_blueprint(product_bp)  

    return app


