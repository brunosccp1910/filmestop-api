from flask import Blueprint, jsonify, request
from filmestop.models import db, Movie, Catalogue_Genre

movies_bp = Blueprint('movies', __name__)


@movies_bp.route('', methods=['POST'])
def create_movie():
    """
    Cria um novo filme

    Cria um novo registro de filme no banco de dados com nome, diretor, ano e gênero.

    ---
    tags:
      - CRUD-Filmes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - director
            - year
            - genre_id
          properties:
            name:
              type: string
              example: "Interestelar"
            director:
              type: string
              example: "Christopher Nolan"
            year:
              type: integer
              example: 2014
            genre_id:
              type: integer
              example: 1
    responses:
      201:
        description: Filme criado com sucesso
      400:
        description: Dados ausentes ou inválidos
    """
    data = request.get_json()
    name = data.get('name')
    director = data.get('director')
    year = data.get('year')
    genre_id = data.get('genre_id')

    if not all([name, director, year, genre_id]):
        return jsonify({'error': 'Missing movie data'}), 400

    try:
        year = int(year)
    except ValueError:
        return jsonify({'error': 'Year must be an integer'}), 400

    genre = Catalogue_Genre.query.get(genre_id)
    if not genre:
        return jsonify({'error': 'Invalid genre_id'}), 400

    new_movie = Movie(name=name, director=director, year=year, genre_id=genre_id)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'message': 'Movie created', 'movie_id': new_movie.id}), 201


@movies_bp.route('', methods=['GET'])
def get_movies():
    """
    Lista todos os filmes

    Retorna todos os filmes cadastrados com seus respectivos dados e nome do gênero.

    ---
    tags:
      - CRUD-Filmes
    responses:
      200:
        description: Lista de filmes retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              director:
                type: string
              year:
                type: integer
              genre:
                type: string
    """
    movies = Movie.query.all()
    return jsonify([
        {
            'id': movie.id,
            'name': movie.name,
            'director': movie.director,
            'year': movie.year,
            'genre': movie.genre.genre_name if movie.genre else None
        }
        for movie in movies
    ])


@movies_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """
    Busca um filme por ID

    Retorna os detalhes de um único filme com base no ID fornecido.

    ---
    tags:
      - CRUD-Filmes
    parameters:
      - name: movie_id
        in: path
        type: integer
        required: true
        description: ID do filme a ser buscado
    responses:
      200:
        description: Detalhes do filme encontrados com sucesso
      404:
        description: Filme não encontrado
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    return jsonify({
        'id': movie.id,
        'name': movie.name,
        'director': movie.director,
        'year': movie.year,
        'genre': movie.genre.genre_name if movie.genre else None
    })


@movies_bp.route('/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """
    Atualiza um filme existente

    Permite atualizar os dados de um filme já cadastrado.

    ---
    tags:
      - CRUD-Filmes
    parameters:
      - name: movie_id
        in: path
        type: integer
        required: true
        description: ID do filme a ser atualizado
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Novo nome do filme"
            director:
              type: string
              example: "Novo Diretor"
            year:
              type: integer
              example: 2020
            genre_id:
              type: integer
              example: 2
    responses:
      200:
        description: Filme atualizado com sucesso
      400:
        description: Gênero inválido
      404:
        description: Filme não encontrado
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    data = request.get_json()
    movie.name = data.get('name', movie.name)
    movie.director = data.get('director', movie.director)
    movie.year = data.get('year', movie.year)
    genre_id = data.get('genre_id', movie.genre_id)

    genre = Catalogue_Genre.query.get(genre_id)
    if not genre:
        return jsonify({'error': 'Invalid genre_id'}), 400

    movie.genre_id = genre_id
    db.session.commit()

    return jsonify({'message': 'Movie updated'})


@movies_bp.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    """
    Deleta um filme

    Remove um filme do banco de dados com base no seu ID.

    ---
    tags:
      - CRUD-Filmes
    parameters:
      - name: movie_id
        in: path
        type: integer
        required: true
        description: ID do filme a ser deletado
    responses:
      200:
        description: Filme deletado com sucesso
      404:
        description: Filme não encontrado
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted'})
