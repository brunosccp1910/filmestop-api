from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache


# Este módulo segue o padrão Singleton para garantir que apenas uma instância de cada extensão
# Instancia o objeto SQLAlchemy.
db = SQLAlchemy()

# Instancia o objeto Migrate.
migrate = Migrate()

# Instancia o objeto de cache com a configuração para usar Redis.
cache = Cache(config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://redis:6379/0'
})