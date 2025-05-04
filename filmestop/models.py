from flask_sqlalchemy import SQLAlchemy
from filmestop.extensions import db


# Define o modelo de usuário
class User(db.Model):
    __tablename__ = 'users'

    # Identificador único do usuário
    id = db.Column(db.Integer, primary_key=True)

    # Nome obrigatório do usuário
    name = db.Column(db.String(50), nullable=False)

    # Email e telefone (opcionais)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(15))

    # Relacionamentos com Rent e Review
    rents = db.relationship('Rent', backref='user', lazy=True)       # Um usuário pode ter vários aluguéis
    reviews = db.relationship('Review', backref='user', lazy=True)   # Um usuário pode fazer várias avaliações


# Define o modelo de filme
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)

    # Nome do filme (obrigatório)
    name = db.Column(db.String(100), nullable=False)

    # Diretor e ano de lançamento (obrigatórios)
    director = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    # Referência obrigatória ao gênero do filme
    genre_id = db.Column(db.Integer, db.ForeignKey('catalogue_genre.id'), nullable=False)

    # Relacionamentos
    genre = db.relationship('Catalogue_Genre', backref='movie')         # Gênero associado
    rents = db.relationship('Rent', backref='movie', lazy=True)         # Aluguéis relacionados
    reviews = db.relationship('Review', backref='movie', lazy=True)     # Avaliações relacionadas

    # Informações agregadas de avaliação
    avg_rate = db.Column(db.Float)            # Média das notas atribuídas ao filme
    count_review = db.Column(db.Integer)      # Total de avaliações recebidas


# Define o catálogo de gêneros
class Catalogue_Genre(db.Model):
    __tablename__ = 'catalogue_genre'

    # Identificador e nome do gênero
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), nullable=False)


# Define o modelo de aluguel de filme
class Rent(db.Model):
    __tablename__ = 'rents'

    id = db.Column(db.Integer, primary_key=True)

    # Chaves estrangeiras obrigatórias: usuário e filme
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    # Informações sobre o aluguel
    start_date = db.Column(db.Date, nullable=False)  # Data de início do aluguel
    rent_days = db.Column(db.Integer)                # Duração do aluguel em dias


# Define o modelo de avaliação (review) de filme
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    # Chaves estrangeiras obrigatórias: usuário e filme
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    # Nota atribuída pelo usuário (0 a 100)
    rate = db.Column(db.Integer, nullable=False)

