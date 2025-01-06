from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from routes.products import product_blueprint
from routes.stock import stock_blueprint
from config import Config
import click
from models.base import db
from logger import logger
from flask import request
from settings import SWAGGER_URL_ENV, SWAGGER_URL_YAML
def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'application/json'
    app.config.from_object(config_class)
    app.register_blueprint(product_blueprint, url_prefix='/api/products')
    app.register_blueprint(stock_blueprint, url_prefix='/api')

    @app.before_request
    def log_request_info():
        logger.info(
            "request_received",
            method=request.method,
            path=request.path,
            remote_addr=request.remote_addr,
        )

    @app.after_request
    def log_response_info(response):
        logger.info(
            "response_sent",
            status=response.status,
            content_type=response.content_type,
            method=request.method,
            path=request.path,
        )
        return response

    # Swagger setup
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL_ENV, SWAGGER_URL_YAML)

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL_ENV)
    db.init_app(app)

    @app.cli.command('init-db')
    def init_db():
        """Inicializa la base de datos creando todas las tablas."""
        db.create_all()
        click.echo('Base de datos inicializada correctamente.')


    @app.cli.command('recreate_db')
    def recreate_db():
        db.drop_all()
        db.create_all()
        db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    # Comando para inicializar la base de datos

    app.run(host='0.0.0.0', port=5000)

    #app.run()