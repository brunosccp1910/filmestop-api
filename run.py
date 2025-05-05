from filmestop import create_app
from seed_data import seed_genres, seed_demo_data
from flask_migrate import upgrade
import time

app = create_app()
print(">>> Iniciando run.py")

if __name__ == '__main__':
    with app.app_context():
        upgrade()          # Aplica as migrations (cria as tabelas)
        seed_genres()  # Apenas popula se as tabelas já existem 
        seed_demo_data() #Cria entradas para as tabelas users,movies,rents e reviews
    app.run(host="0.0.0.0", port=5000, debug=True)