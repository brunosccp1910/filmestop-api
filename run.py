from filmestop import create_app
from seed_data import seed_genres  # A importação de seed_genres deve funcionar aqui
from filmestop.extensions import db
import time

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()       # Garante que todas as tabelas existem
        seed_genres()         # Popula os dados iniciais
    app.run(host="0.0.0.0", port=5000, debug=True)