from flask import Blueprint, jsonify, request
from ..models import User, Movie, Catalogue_Genre, Rent , Review
from datetime import datetime
from sqlalchemy import text
from filmestop.extensions import db, cache
import time

main = Blueprint('main', __name__)


def recalculate_movie_rating(movie_id):
    
    """
    Recalcula os campos de média de avaliação de filme e incrementa o contador de avaliações

    Returns:
        Response 200 com mensagem de sucesso.
    """
    reviews = Review.query.filter_by(movie_id=movie_id).all()

    if not reviews:
        avg_rate = 0
        count_review = 0
    else:
        total = sum([review.rate for review in reviews])
        count_review = len(reviews)
        avg_rate = total / count_review

    # Atualiza o filme
    movie = db.session.get(Movie, movie_id)
    movie.avg_rate = round(avg_rate, 2)
    movie.count_review = count_review

    db.session.commit()
    return {'message': 'Movie rating recalculated', 'new_avg_rate': avg_rate}, 200



#feature 1 - O usuário deve ser capaz de visualizar a lista de filmes disponíveis por gênero;

@main.route('/movies', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_movies_by_genre():
    """
    Lista todos os filmes ou filtra por gênero

    Este endpoint atende ao requisito 1 do Case.

    - Se nenhum parâmetro for informado, retorna todos os filmes cadastrados.
    - Se `genre_id` for fornecido, retorna apenas os filmes desse gênero.

    ---
    tags:
      - case-Filmes
    parameters:
      - name: genre_id
        in: query
        type: integer
        required: false
        description: ID do gênero para filtrar filmes
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
                example: 1
              name:
                type: string
                example: "Titanic"
              director:
                type: string
                example: "Leonardo"
              year:
                type: integer
                example: 1999
              genre:
                type: string
                example: "Drama"
      400:
        description: O parâmetro genre_id não é um número válido
        schema:
          type: object
          properties:
            error:
              type: string
              example: "genre_id must be an integer"
      404:
        description: Nenhum filme encontrado para o gênero informado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No movies found for genre id: 99"
    """
    genre_id = request.args.get('genre_id')

    if genre_id is None:
        # Lista completa de filmes
        movies = Movie.query.all()
        return jsonify([{
            'id': m.id,
            'name': m.name,
            'director': m.director,
            'year': m.year,
            'genre': m.genre.genre_name if m.genre else None
        } for m in movies]), 200

    try:
        genre_id = int(genre_id)
    except ValueError:
        return jsonify({'error': 'genre_id must be an integer'}), 400

    movies = Movie.query.filter_by(genre_id=genre_id).all()
    if not movies:
        return jsonify({'error': f'No movies found for genre id: {genre_id}'}), 404

    return jsonify([{
        'id': m.id,
        'name': m.name,
        'director': m.director,
        'year': m.year,
        'genre': m.genre.genre_name if m.genre else None
    } for m in movies]), 200


#feature 2 - o usuário deve ser capaz de listar todas as informações sobre um determinado filme;
@main.route('/movies/<int:movie_id>', methods=['GET'])
@cache.cached(timeout=60)
def get_movie_by_id(movie_id):
    """
    Retorna os detalhes de um filme específico

    Este endpoint atende ao requisito 2 do Case.

    ---
    tags:
      - case-Filmes
    parameters:
      - name: movie_id
        in: path
        type: integer
        required: true
        description: ID do filme
    responses:
      200:
        description: Filme encontrado com sucesso
      404:
        description: Filme não encontrado
    """
    movie = db.session.get(Movie, movie_id)

    if not movie:
        return jsonify({'message': f'There is no movie with the ID: {movie_id}'}), 404

    return jsonify({
        'id': movie.id,
        'name': movie.name,
        'director': movie.director,
        'year': movie.year,
        'genre': movie.genre.genre_name if movie.genre else None
    }), 200


#feature 3  O usuário deve ser capaz de alugar um filme - New migration for Rent table 

@main.route('/users/<int:user_id>/movies/<int:movie_id>/rent', methods=['POST'])
def rent_movie(user_id, movie_id):
    """
    Realiza o aluguel de um filme

    Este endpoint contempla o item 3 dos requisitos obrigatório do Case.
    Cria um novo aluguel associando um usuário a um filme por um período específico.

    ---
    tags:
      - case-Aluguéis
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
        description: ID do usuário
      - name: movie_id
        in: path
        required: true
        type: integer
        description: ID do filme
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - start_date
            - rent_days
          properties:
            start_date:
              type: string
              format: date
              example: "2025-01-01"
            rent_days:
              type: integer
              example: 3
    responses:
      201:
        description: Aluguel criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
            rent:
              type: object
              properties:
                id:
                  type: integer
                user_id:
                  type: integer
                movie_id:
                  type: integer
                start_date:
                  type: string
                rent_days:
                  type: integer
      400:
        description: Dados inválidos
      404:
        description: Usuário ou filme não encontrado
    """
    rent_data = request.get_json()
    start_date = rent_data.get('start_date')
    rent_days = rent_data.get('rent_days')

    if not all([start_date, rent_days]):
        return jsonify({'error': 'Missing rent information'}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD'}), 400

    user = db.session.get(User, user_id)
    movie = db.session.get(Movie, movie_id)

    if not user:
        return jsonify({'error': 'User id not found'}), 404
    if not movie:
        return jsonify({'error': 'Movie id not found'}), 404

    new_rent = Rent(
        user_id=user_id,
        movie_id=movie_id,
        start_date=start_date,
        rent_days=rent_days
    )
    db.session.add(new_rent)
    db.session.commit()

    return jsonify({
        'message': 'Successfully created new movie rent',
        'rent': {
            'id': new_rent.id,
            'user_id': new_rent.user_id,
            'movie_id': new_rent.movie_id,
            'start_date': new_rent.start_date.isoformat(),
            'rent_days': new_rent.rent_days
        }
    }), 201

#feature 4 - o usuário deve ser capaz de associar uma nota a cada filme já alugado;
@main.route('/users/<int:user_id>/movies/<int:movie_id>/review', methods=['POST'])
def set_review_rate(user_id, movie_id):
    """
    Avalia um filme alugado

    Permite que um usuário avalie um filme que ele alugou, ou atualize sua avaliação.
    Este endpoint contempla o item 4 dos requisitos obrigatórios do Case.

    ---
    tags:
      - case-Avaliações
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
        description: ID do usuário
      - name: movie_id
        in: path
        required: true
        type: integer
        description: ID do filme
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - rate
          properties:
            rate:
              type: integer
              minimum: 0
              maximum: 100
              example: 80
    responses:
      200:
        description: Avaliação salva com sucesso
      400:
        description: Dados inválidos
      403:
        description: Avaliação não permitida (filme não alugado)
      404:
        description: Usuário ou filme não encontrado
    """
    data = request.get_json()
    rate = data.get('rate')

    if rate is None:
        return jsonify({'error': 'Missing review information'}), 400

    try:
        rate = int(rate)
        if not 0 <= rate <= 100:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Rate must be an integer between 0 and 100'}), 400

    user = db.session.get(User, user_id)
    movie = db.session.get(Movie, movie_id)

    if not user or not movie:
        return jsonify({'error': 'User or movie not found'}), 404

    rented = Rent.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not rented:
        return jsonify({'error': 'You can only rate movies you have rented'}), 403

    existing_review = Review.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if existing_review:
        existing_review.rate = rate
    else:
        new_review = Review(user_id=user_id, movie_id=movie_id, rate=rate)
        db.session.add(new_review)

    db.session.commit()

    response, status = recalculate_movie_rating(movie_id)
    return jsonify({
        'message': 'Review saved and movie rating updated',
        'rating_info': response
    }), status

# feature 5 -  usuário deve ser capaz de visualizar todos os filmes que ele já alugou com as notas que ele atribuiu para cada filme e a data de locação.
@main.route('/users/<int:user_id>/rented_movies', methods=['GET'])
def get_rented_movies(user_id):
    """
    Lista os filmes alugados por um usuário

    Este endpoint contempla o item 5 dos requisitos obrigatórios do Case.

    Retorna todos os filmes que um usuário já alugou, junto com as notas atribuídas (caso existam) e a data do aluguel.

    ---
    tags:
      - case-Aluguéis
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário
        example: 1
    responses:
      200:
        description: Lista de filmes alugados
        schema:
          type: array
          items:
            type: object
            properties:
              rent_id:
                type: integer
                example: 12
              movie_name:
                type: string
                example: "Matrix"
              rent_start_date:
                type: string
                format: date
                example: "2025-01-01"
              movie_rating:
                type: integer
                example: 85
      400:
        description: Parâmetro inválido
    """
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'error': 'User ID must be an integer'}), 400

    query = text("""
        SELECT 
            m.name AS movie_name,
            r.start_date AS rent_start_date,
            r.id AS rent_id,
            rev.rate AS movie_rating
        FROM 
            rents r
        JOIN 
            movies m ON r.movie_id = m.id
        LEFT JOIN 
            reviews rev ON r.movie_id = rev.movie_id AND r.user_id = rev.user_id
        WHERE 
            r.user_id = :user_id
    """)

    result = db.session.execute(query, {'user_id': user_id})
    movies = [
        {
            'rent_id': row.rent_id,
            'movie_name': row.movie_name,
            'rent_start_date': row.rent_start_date,
            'movie_rating': row.movie_rating
        }
        for row in result
    ]

    return jsonify(movies), 200
