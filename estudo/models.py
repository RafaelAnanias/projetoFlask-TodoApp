from estudo import db, login_manager
from datetime import datetime
from flask_login import UserMixin


# Função usada pelo Flask-Login para carregar o usuário pela sessão
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Garante que seja um número inteiro


# Modelo do Usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  # Melhor exigir preenchimento
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Garante e-mail único
    senha = db.Column(db.String(200), nullable=False)  # Armazenará hash seguro

    # Relacionamento com a tabela Lista
    listas = db.relationship('Lista', backref='usuario', lazy=True)


# Modelo da Tarefa (Lista)
class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(100), nullable=False)

    # Chave estrangeira para vincular ao usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)















