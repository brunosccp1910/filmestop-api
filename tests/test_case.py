from datetime import date
from filmestop import create_app, db
from filmestop.models import User, Movie, Rent, Review, Catalogue_Genre

"""
Testes para a Feature 1: listagem de filmes por gênero.

Cenários testados:
- Quando o genre_id é válido e há filmes disponíveis.
- Quando o genre_id é válido mas não há filmes.
- Quando o genre_id não é um número inteiro.
"""

def test_get_movies_by_valid_genre(client, setup_sample_data):
    user, movie, genre, _ = setup_sample_data
    response = client.get(f'/case/movies?genre_id={genre.id}')

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(f['id'] == movie.id for f in data)

def test_get_movies_by_invalid_genre_id(client):
    response = client.get('/case/movies?genre_id=999')
    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert 'error' in data
    assert 'No movies found for genre id' in data['error']

def test_get_movies_by_non_integer_genre_id(client):
    response = client.get('/case/movies?genre_id=test')
    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert 'error' in data
    assert 'genre_id must be an integer' in data['error']

""" Testes da Feature 2: Obter detalhes de um filme.
Cenários:
- Quando o ID do filme é válido
- Quando o ID do filme é inválido
- Quando o ID informado não é um número inteiro
"""


def test_get_movies_by_valid_movie_id(client, setup_sample_data):
    """Retorna detalhes do filme com ID válido"""
    user, movie, _, _ = setup_sample_data
    response = client.get(f'/case/movies/{movie.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['id'] == movie.id

def test_get_movies_by_invalid_movie_id(client):
    """Retorna 404 ao buscar um ID de filme inexistente"""
    response = client.get('/case/movies/999')
    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert 'There is no movie with the ID' in data['message']

def test_get_movies_by_non_integer_movie_id(client):
    # Rota espera <int:movie_id>, portanto Flask retorna 404 direto sem entrar na view
    response = client.get('/case/movies/test')
    assert response.status_code == 404

"""
Testes da Feature 3: Aluguel de filmes

Cenários testados:
- Criação bem-sucedida de aluguel com dados válidos
- Falha ao omitir informações obrigatórias
- Falha ao fornecer movie_id inexistente
- Falha ao fornecer user_id inexistente
- Falha ao fornecer data em formato inválido
"""

def test_post_valid_rent(client, setup_sample_data):
    """Cria um novo aluguel com sucesso usando dados válidos"""
    user, movie, _, _ = setup_sample_data
    new_start_date = date(2025, 1, 10)

    response = client.post(f'/case/users/{user.id}/movies/{movie.id}/rent', json={
        'start_date': new_start_date.isoformat(),
        'rent_days': 5
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Successfully created new movie rent'
    rent_data = data['rent']
    assert rent_data['user_id'] == user.id
    assert rent_data['movie_id'] == movie.id
    assert rent_data['start_date'] == new_start_date.isoformat()
    assert rent_data['rent_days'] == 5


def test_post_miss_info_rent(client, setup_sample_data):
    """Retorna erro 400 ao omitir o campo start_date no aluguel"""
    user, movie, _, _ = setup_sample_data

    response = client.post(f'/case/users/{user.id}/movies/{movie.id}/rent', json={
        'rent_days': 5
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing rent information'


def test_post_invalid_movie_id_rent(client, setup_sample_data):
    """Retorna erro 404 ao tentar alugar um filme com movie_id inexistente"""
    user, _, _, _ = setup_sample_data
    new_start_date = date(2025, 1, 10)

    response = client.post(f'/case/users/{user.id}/movies/9999/rent', json={
        'start_date': new_start_date.isoformat(),
        'rent_days': 5
    })

    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Movie id not found'


def test_post_invalid_user_id_rent(client, setup_sample_data):
    """Retorna erro 404 ao tentar alugar um filme com user_id inexistente"""
    _, movie, _, _ = setup_sample_data
    new_start_date = date(2025, 1, 10)

    response = client.post(f'/case/users/9999/movies/{movie.id}/rent', json={
        'start_date': new_start_date.isoformat(),
        'rent_days': 5
    })

    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'User id not found'


def test_post_invalid_date_rent(client, setup_sample_data):
    """Retorna erro 400 ao fornecer data em formato inválido (não ISO)"""
    user, movie, _, _ = setup_sample_data
    invalid_date = "01/09/1996"

    response = client.post(f'/case/users/{user.id}/movies/{movie.id}/rent', json={
        'start_date': invalid_date,
        'rent_days': 5
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid start_date format. Use YYYY-MM-DD'

"""
Testes da Feature 4: Avaliação de filmes

Cenários testados:
- Criação de avaliação com dados válidos
- Falha ao omitir informações obrigatórias
- Falha ao fornecer uma nota fora do intervalo permitido
- Falha ao tentar avaliar um filme que não foi alugado pelo usuário
"""

def test_post_valid_review(client, setup_sample_data):
    """Cria uma avaliação com sucesso para um filme já alugado"""
    user, movie, _, _ = setup_sample_data
    new_rate = 5

    response = client.post(f'/case/users/{user.id}/movies/{movie.id}/review', json={
        'rate': new_rate
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Review saved and movie rating updated'


def test_post_miss_info_review(client, setup_sample_data):
    """Retorna erro 400 ao omitir o campo rate na avaliação"""
    user, movie, _, _ = setup_sample_data

    response = client.post(f'/case/users/{user.id}/movies/{movie.id}/review', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing review information'


def test_post_invalid_rate_review(client, setup_sample_data):
    """Retorna erro 400 ao fornecer nota fora do intervalo permitido (0-100)"""
    user, movie, _, _ = setup_sample_data
    new_rate = 101

    response = client.post(f'/case/users/{user.id}/movies/{movie.id}/review', json={
        'rate': new_rate
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Rate must be an integer between 0 and 100'


def test_user_cannot_review_unrented_movie(client, setup_sample_data):
    """Retorna erro 403 quando o usuário tenta avaliar um filme que não alugou"""
    user, _, genre, _ = setup_sample_data

    # Cria um novo filme que o usuário não alugou
    new_movie = Movie(name='Teste movie 2', director='Dir', year=2020, genre_id=genre.id)
    db.session.add(new_movie)
    db.session.commit()

    response = client.post(f'/case/users/{user.id}/movies/{new_movie.id}/review', json={
        'rate': 80
    })

    assert response.status_code == 403
    data = response.get_json()
    assert data['error'] == 'You can only rate movies you have rented'


"""
Testes da Feature 5: Listagem de filmes alugados por um usuário

Cenários testados:
- Consulta bem-sucedida dos filmes alugados com nota
- Falha ao omitir o parâmetro obrigatório user_id
- Falha ao fornecer um user_id inválido (não inteiro)
"""
def test_get_rented_movies_by_valid_user_id(client, setup_sample_data):
    """Retorna com sucesso os filmes alugados por um usuário com suas respectivas avaliações"""
    user, movie, _, rent = setup_sample_data

    # Cria uma avaliação para o filme alugado
    new_review = Review(user_id=user.id, movie_id=movie.id, rate=99)
    db.session.add(new_review)
    db.session.commit()

    response = client.get(f'/case/users/{user.id}/rented_movies')
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['rent_id'] == rent.id
    assert data[0]['movie_name'] == movie.name
    assert data[0]['rent_start_date'] == rent.start_date.isoformat()
    assert data[0]['movie_rating'] == new_review.rate


def test_get_rented_movies_invalid_user_id(client):
    """Retorna erro 404 ao fornecer user_id inválido (não numérico na URL)"""
    response = client.get('/case/users/test/rented_movies')
    assert response.status_code == 404  # Flask não encontra rota com user_id não inteiro


def test_get_rented_movies_nonexistent_user(client):
    """Retorna lista vazia para um usuário inexistente com ID numérico válido"""
    response = client.get('/case/users/9999/rented_movies')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data == []  # sem aluguéis registrados