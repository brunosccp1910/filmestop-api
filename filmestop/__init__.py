from flask import Flask
from flasgger import Swagger
from flask import jsonify

from filmestop.extensions import db, migrate, cache
from filmestop.routes.case_requirements import main
from filmestop.routes.users import users_bp
from filmestop.routes.movies import movies_bp
from filmestop.config import Config, TestingConfig

def create_app(config_name='default'):
    app = Flask(__name__)

    # Carrega a configuração com base no ambiente ('testing' ou produção)
    app.config.from_object(TestingConfig if config_name == 'testing' else Config)

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    # Inicializa o Swagger (documentação automática dos endpoints)
    Swagger(app) 
    
    # Tratando endpoints inválidos
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'API endpoint not found. Please verify the path.'}), 404


    # Registra os blueprints da aplicação
    app.register_blueprint(main, url_prefix='/case')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(movies_bp, url_prefix='/movies')

    return app
