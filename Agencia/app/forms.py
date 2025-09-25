from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, IntegerField,BooleanField,SelectField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime


bcrypt=Bcrypt()


import os
from werkzeug.utils import secure_filename


from app import db, Bcrypt
from app.models import User, Pacotes, Fechamento


class UserForm (FlaskForm):
    nome = StringField ('Nome', validators=[DataRequired()])
    sobrenome = StringField ('Sobrenome', validators=[DataRequired()])
    email = StringField ('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já cadastrado.')


    def save (self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User (
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha.decode('utf-8')
        )


        db.session.add(user)
        db.session.commit()
        return (user)
   
class LoginForm (FlaskForm):
    email = StringField ('E-mail', validators=[DataRequired(),Email()])
    senha = PasswordField ('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')


    def login (self):
       
        user = User.query.filter_by (email=self.email.data).first()


        if user:
            if bcrypt.check_password_hash (user.senha, self.senha.data.encode ('utf-8')):
              
                return user
            else:
                raise Exception ('Senha incorreta!')
           
        else:
            raise Exception ('Usuário não encontrado!')


class PacoteForm (FlaskForm):
    Nome = StringField ('Nome', validators=[DataRequired()])
    Pessoas = IntegerField ('Quantidade de pessoas no pacote', validators=[DataRequired()])
    Destino = StringField ('Destino', validators=[DataRequired()])
    preco = IntegerField ('Preços', validators=[DataRequired()])
    disponibilidade = BooleanField('Disponível')
    categoria = StringField ('categoria', validators=[DataRequired()])
    btnSubmit = SubmitField('Cadastrar')


    def save (self):
        pacotes = Pacotes (
            Nome = self.Nome.data,
            Pessoas = self.Pessoas.data,
            Destino = self.Destino.data,
            preco = self.preco.data,
            disponibilidade=self.disponibilidade.data,
            categoria = self.categoria.data
            
        )
       
        db.session.add(pacotes)
        db.session.commit()
        return pacotes

class FechamentoForm(FlaskForm):
    data_partida = DateField('Data da Partida', format='%Y-%m-%d', validators=[DataRequired()])
    data_retorno = DateField('Data do Retorno', format='%Y-%m-%d', validators=[DataRequired()])
    User_id = SelectField('Usuário', coerce=int, validators=[DataRequired()])
    Pacotes_id = SelectField('Livro', coerce=int, validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.User_id.choices = [(u.id, u.nome) for u in User.query.all()]
        self.Pacotes_id.choices = [(l.id, l.Nome) for l in Pacotes.query.all()]
    
    def save(self):

        fechamento = Fechamento(
            data_partida = self.data_partida.data,
            data_retorno = self.data_retorno.data,
            User_id = self.User_id.data,
            Pacotes_id = self.Pacotes_id.data
        )

        db.session.add(fechamento)
        db.session.commit()