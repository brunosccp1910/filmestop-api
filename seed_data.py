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
    print("Verificando usuários existentes...")
    existing_emails = {u.email for u in User.query.all()}
    users_data = [
        {"name": "Bruno Silva", "email": "bruno@email.com", "phone": "99999-0001"},
        {"name": "Jack Antônio", "email": "jack@email.com", "phone": "99999-0002"},
        {"name": "Hellen Barros", "email": "hellen@email.com", "phone": "99999-0003"},
        {"name": "Maria Silva", "email": "maria@email.com", "phone": "99999-0004"},
        {"name": "Francisco Ferreira", "email": "francisco@email.com", "phone": "99999-0005"},
    ]

    users = []
    for user_data in users_data:
        if user_data["email"] not in existing_emails:
            user = User(**user_data)
            db.session.add(user)
            users.append(user)

    db.session.commit()
    print(f"{len(users)} novos usuários inseridos.")

    # Gêneros já devem existir
    genres = {g.genre_name: g.id for g in Catalogue_Genre.query.all()}
    print("Gêneros encontrados:", genres)

    print("Verificando filmes existentes...")
    existing_movies = {m.name for m in Movie.query.all()}
    filmes_data = [
        ("Matrix", "Wachowski", 1999, "Action"),
        ("Titanic", "James Cameron", 1997, "Romance"),
        ("Avatar", "James Cameron", 2009, "Sci-Fi"),
        ("O Auto da Compadecida", "Guel Arraes", 2000, "Comedy"),
        ("Coringa", "Todd Phillips", 2019, "Drama"),
        ("Inception", "Christopher Nolan", 2010, "Action"),
        ("A Origem", "Christopher Nolan", 2010, "Sci-Fi"),
        ("O Poderoso Chefão", "Francis Ford Coppola", 1972, "Drama"),
        ("Cidade de Deus", "Fernando Meirelles", 2002, "Drama"),
        ("Parasita", "Bong Joon-ho", 2019, "Thriller"),
    ]

    for name, director, year, genre in filmes_data:
        if name not in existing_movies:
            genre_id = genres.get(genre, 1)
            movie = Movie(name=name, director=director, year=year, genre_id=genre_id)
            db.session.add(movie)

    db.session.commit()
    print("Filmes atualizados.")

    # Aluguéis (usuarios 1 a 3)
    all_users = User.query.limit(3).all()
    all_movies = Movie.query.all()
    rents = []
    user_rented_movies = {user.id: [] for user in all_users}

    for user in all_users:
        rented_movies = random.sample(all_movies, k=5)
        for movie in rented_movies:
            if not Rent.query.filter_by(user_id=user.id, movie_id=movie.id).first():
                start = date(2025, 1, random.randint(1, 20))
                rent = Rent(user_id=user.id, movie_id=movie.id, start_date=start, rent_days=random.randint(1, 7))
                rents.append(rent)
                user_rented_movies[user.id].append(movie.id)

    db.session.add_all(rents)
    db.session.commit()
    print("Aluguéis inseridos.")

    # Avaliações (somente filmes alugados)
    reviews = []
    for user in all_users:
        for movie_id in user_rented_movies[user.id]:
            if random.random() < 0.7:
                if not Review.query.filter_by(user_id=user.id, movie_id=movie_id).first():
                    review = Review(user_id=user.id, movie_id=movie_id, rate=random.randint(50, 100))
                    reviews.append(review)

    db.session.add_all(reviews)
    db.session.commit()
    print("Avaliações inseridas.")