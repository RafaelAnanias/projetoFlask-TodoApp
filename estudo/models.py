from estudo import db, login_manager
from datetime import datetime
from flask_login import UserMixin #Serve para informar qual modelo vamos utilizar para o cadastro

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(user_id)
class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     nome = db.Column(db.String(100), nullable=True)
     sobrenome = db.Column(db.String(100), nullable=True)
     email = db.Column(db.String(100), nullable=True)
     senha = db.Column(db.String(100), nullable=True)
      # Relacionamento com a tabela Lista
     listas = db.relationship('Lista', backref='usuario', lazy=True)
class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(100), nullable=True) 
    
     # Chave estrangeira para referenciar o usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    