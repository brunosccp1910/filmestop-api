# seed_data.py
from filmestop.models import  Catalogue_Genre  # Certifique-se de importar corretamente o db e o modelo
from filmestop.extensions import db


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
