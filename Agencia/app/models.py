
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user (user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)

  

class Pacotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Pessoas = db.Column(db.String, nullable=True)
    Nome = db.Column(db.String, nullable=True)
    Destino = db.Column(db.String, nullable=True)
    preco = db.Column(db.Integer, nullable=True)
    disponibilidade = db.Column(db.Boolean, default=True, nullable=False)
    categoria = db.Column(db.String, nullable=True)

    
    
class Fechamento(db.Model):
    __tablename__ = "fechamento"
    id = db.Column(db.Integer, primary_key=True)
    data_partida = db.Column(db.DateTime, default=datetime.now)
    data_retorno = db.Column(db.DateTime, default=datetime.now)
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    Pacotes_id = db.Column(db.Integer, db.ForeignKey('pacotes.id'), nullable=True)

    User = db.relationship("User", backref=db.backref("fechamentos", lazy=True))
    Pacotes = db.relationship("Pacotes", backref=db.backref("fechamentos", lazy=True))
