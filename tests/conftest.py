import pytest
import sys
import os
from datetime import date

# Garante que o diretório raiz esteja no PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from filmestop import create_app
from filmestop.extensions import db

from filmestop.models import User, Movie, Rent, Review, Catalogue_Genre
from seed_data import seed_genres


@pytest.fixture
def app():
    """
    Cria uma instância da aplicação Flask configurada para testes,
    com banco de dados em memória SQLite

    Responsável por:
    - Criar todas as tabelas
    - Popular os gêneros com `seed_genres`
    - Limpar tudo após os testes com `drop_all`
    """
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        seed_genres()  # Insere os gêneros no banco
        yield app      # Disponibiliza a app para os testes
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Fornece um client de testes para simular requisições HTTP.
    É usado em todos os testes com o parâmetro `client`.
    """
    return app.test_client()


@pytest.fixture
def setup_sample_data(app):
    """
    Preenche o banco de dados com dados consistentes para testes:
    - Cria um usuário
    - Cria um filme de gênero 'Action'
    - Cria um aluguel relacionado ao usuário e ao filme

    Retorna: tupla (user, movie, genre, rent)
    """
    user = User(name='Test User', email='test@example.com', phone='9888888888')
    db.session.add(user)
    db.session.commit()

    genre = Catalogue_Genre.query.filter_by(genre_name='Action').first()

    movie = Movie(name='Test Movie', director='Test Director', year=2010, genre_id=genre.id)
    db.session.add(movie)
    db.session.commit()

    rent = Rent(user_id=user.id, movie_id=movie.id, start_date=date(2025, 1, 1), rent_days=3)
    db.session.add(rent)
    db.session.commit()

    return user, movie, genre, rent