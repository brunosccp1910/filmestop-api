from flask import Blueprint, jsonify, request
from filmestop.models import db, User
import re

users_bp = Blueprint('users', __name__)

def validate_email(email):
    # Função para validar o formato de e-mail
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


@users_bp.route('', methods=['POST'])
def create_user():
    """
    Cria um novo usuário

    Registra um novo usuário com nome, email e telefone.

    ---
    tags:
      - CRUD-Usuários
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - phone
          properties:
            name:
              type: string
              example: "Bruno Silva"
            email:
              type: string
              example: "bruno@email.com"
            phone:
              type: string
              example: "99999-9999"
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Dados inválidos ou ausentes
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    if not email or not validate_email(email):
        return jsonify({'error': 'Valid email is required'}), 400

    if not phone:
        return jsonify({'error': 'Valid phone number is required'}), 400

    new_user = User(name=name, email=email, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created', 'user_id': new_user.id}), 201


@users_bp.route('', methods=['GET'])
def get_users():
    """
    Lista todos os usuários

    Retorna todos os usuários cadastrados no sistema.

    ---
    tags:
      - CRUD-Usuários
    responses:
      200:
        description: Lista de usuários
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
              phone:
                type: string
    """
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone
    } for user in users])


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Busca um usuário por ID

    Retorna os dados de um usuário específico pelo ID fornecido.

    ---
    tags:
      - CRUD-Usuários
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Dados do usuário encontrados
      404:
        description: Usuário não encontrado
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'phone': user.phone})


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Atualiza os dados de um usuário

    Permite atualizar nome, email e telefone de um usuário.

    ---
    tags:
      - CRUD-Usuários
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Bruno Silva"
            email:
              type: string
              example: "bruno@email.com"
            phone:
              type: string
              example: "99999-9999"
    responses:
      200:
        description: Usuário atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Usuário não encontrado
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    name = data.get('name', user.name)
    email = data.get('email', user.email)
    phone = data.get('phone', user.phone)

    if not email or not validate_email(email):
        return jsonify({'error': 'Valid email is required'}), 400

    if not phone:
        return jsonify({'error': 'Valid phone number is required'}), 400

    user.name = name
    user.email = email
    user.phone = phone

    db.session.commit()
    return jsonify({'message': 'User updated'})


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Remove um usuário

    Exclui permanentemente um usuário com base no seu ID.

    ---
    tags:
      - CRUD-Usuários
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
        description: ID do usuário
    responses:
      200:
        description: Usuário deletado com sucesso
      404:
        description: Usuário não encontrado
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
