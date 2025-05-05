# TopFilmes API

Uma API desenvolvida para avaliação de Case técnico.

##  Estrutura do Projeto

```
filmestop/
├── routes/                # Rotas divididas por domínio (case, usuários, filmes)
│   ├── case_requirements.py
│   ├── users.py
│   └── movies.py
├── config.py              # Configurações de ambiente
├── extensions.py          # Extensões compartilhadas (db, cache, migrate)
├── models.py              # Modelos SQLAlchemy
├── __init__.py            # Inicialização da aplicação Flask
migrations/                # Arquivos de migração gerados pelo Flask-Migrate
tests/
├── conftest.py            # Fixtures do Pytest
├── test_case.py           # Testes automatizados para os requisitos do case
Dockerfile                 # Dockerfile para construir a imagem da aplicação
docker-compose.yml         # Orquestração dos containers (PostgreSQL, Redis, App)
run.py                     # Entrada principal da aplicação Flask
seed_data.py               # Script de seed dos gêneros iniciais e inserção no banco para testes
requirements.txt           # Dependências da aplicação
README.md                  # Documentação do projeto
```

##  Tecnologias Utilizadas

- Python 3.10
- Flask
- SQLAlchemy
- PostgreSQL
- Redis (Flask-Caching)
- Pytest
- Docker / Docker Compose
- Flasgger (Swagger UI)



##  Como rodar com Docker
> São inseridos alguns dados iniciais para facilitar a validação de funcionalidade. Cinco usuários foram criados, bem como 10 filmes, alugueis e avaliações.
> Para rodar, na raiz do projeto execute:

```bash
docker-compose up --build
```

Acesse a aplicação em `http://localhost:5000`.

##  Testes

Execute os testes com:
> Os testes são executados com SQLite em memória para performance.
> Para rodar os testes separadamente:


```bash
docker-compose run --rm test
```

##  Documentação Swagger

A documentação automática dos endpoints está disponível em:

```
http://localhost:5000/apidocs
```

##  Funcionalidades


- [x] Aluguel de filmes
- [x] Avaliação de filmes alugados
- [x] Listagem de filmes por gênero e ID 
- [x] Visualização de histórico de filmes alugados e notas atribuídas
- [x] CRUD de usuários
- [x] CRUD de filmes

##  Padrões adotados

- **Factory Pattern**: `create_app` permite diferentes configs (produção/testes).
- **Singleton Pattern**: extensões como `db`, `cache`, `migrate` são singletons via `extensions.py`.
- **Camada de rotas separada por domínio**.
- **Cache com Redis** para rotas de leitura na listagem de filmes.
- **Documentação automática** com Flasgger.

---

