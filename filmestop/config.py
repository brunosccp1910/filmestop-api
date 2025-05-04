
# Classe base de configuração para o ambiente padrão da aplicação.
class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:pass@psql-db:5432/topfilmesdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://redis:6379/0"

# Classe de configuração específica para testes automatizados.
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'null'