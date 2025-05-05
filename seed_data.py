from filmestop.extensions import db
from filmestop.models import db, User, Movie, Rent, Review, Catalogue_Genre
from datetime import date, timedelta
import random



def seed_genres():
    genres = [
         'Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Fantasy', 'Thriller', 'Documentary', 'Animation'
     ]

    for genre_name in genres:
         # Verifica se o gênero já existe
         if not Catalogue_Genre.query.filter_by(genre_name=genre_name).first():
             genre = Catalogue_Genre(genre_name=genre_name)
             db.session.add(genre)

    db.session.commit()

def seed_demo_data():
        # Usuários
        users = [
            User(name="Bruno Silva", email="bruno@email.com", phone="99999-0001"),
            User(name="Jack Antônio", email="jack@email.com", phone="99999-0002"),
            User(name="Hellen Barros", email="hellen@email.com", phone="99999-0003"),
            User(name="Maria Silva", email="maria@email.com", phone="99999-0004"),
            User(name="Francisco Ferreira", email="francisco@email.com", phone="99999-0005")
        ]
        print("Inserindo usuários...")

        db.session.add_all(users)
        db.session.commit()
        print("Usuários inseridos com sucesso.")

        # Gêneros já devem existir no banco
        genres = {g.genre_name: g.id for g in Catalogue_Genre.query.all()}
        print("Gêneros encontrados:", genres)

        # Filmes
        print("Inserindo filmes...")

        filmes = [
            Movie(name="Matrix", director="Wachowski", year=1999, genre_id=genres.get("Action", 1)),
            Movie(name="Titanic", director="James Cameron", year=1997, genre_id=genres.get("Romance", 2)),
            Movie(name="Avatar", director="James Cameron", year=2009, genre_id=genres.get("Sci-Fi", 3)),
            Movie(name="O Auto da Compadecida", director="Guel Arraes", year=2000, genre_id=genres.get("Comedy", 4)),
            Movie(name="Coringa", director="Todd Phillips", year=2019, genre_id=genres.get("Drama", 5)),
            Movie(name="Inception", director="Christopher Nolan", year=2010, genre_id=genres.get("Action", 1)),
            Movie(name="A Origem", director="Christopher Nolan", year=2010, genre_id=genres.get("Sci-Fi", 3)),
            Movie(name="O Poderoso Chefão", director="Francis Ford Coppola", year=1972, genre_id=genres.get("Drama", 5)),
            Movie(name="Cidade de Deus", director="Fernando Meirelles", year=2002, genre_id=genres.get("Drama", 5)),
            Movie(name="Parasita", director="Bong Joon-ho", year=2019, genre_id=genres.get("Thriller", 6))
        ]
        db.session.add_all(filmes)
        db.session.commit()
        print("Filmes inseridos com sucesso.")

        # Aluguéis (apenas usuários 1, 2 e 3)
        all_users = User.query.limit(3).all()
        all_movies = Movie.query.all()
        rents = []
        user_rented_movies = {user.id: [] for user in all_users}

        for user in all_users:
            rented_movies = random.sample(all_movies, k=5)  # cada um aluga 5 filmes
            for movie in rented_movies:
                start = date(2025, 1, random.randint(1, 20))
                rent = Rent(user_id=user.id, movie_id=movie.id, start_date=start, rent_days=random.randint(1, 7))
                rents.append(rent)
                user_rented_movies[user.id].append(movie.id)  # salva quais filmes ele alugou

        db.session.add_all(rents)
        db.session.commit()
        print("Aluguéis inseridos com sucesso.")

        # Avaliações (somente dos filmes alugados)
        reviews = []
        for user in all_users:
            for movie_id in user_rented_movies[user.id]:
                if random.random() < 0.7:  # nem todo filme alugado precisa ser avaliado
                    rate = random.randint(50, 100)
                    review = Review(user_id=user.id, movie_id=movie_id, rate=rate)
                    reviews.append(review)

        db.session.add_all(reviews)
        db.session.commit()
        print("Avaliações inseridas com sucesso.")
