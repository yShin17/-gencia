from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import UserForm, LoginForm,PacoteForm,FechamentoForm
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_
from app.models import Pacotes,Fechamento,User
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import String
from datetime import datetime



@app.route('/')
def homepage():
    return render_template('index.html', mostrar_imagem=True)


@app.route ('/login', methods=['GET', 'POST'])
def LoginPage ():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login ()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template ("usuario_login.html", form=form)



@app.route ('/cadastro', methods=['GET', 'POST'])
def RegisterPage ():
    form = UserForm ()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template ("usuario_cadastro.html", form=form)



@app.route('/sair/')
@login_required
def logout ():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/pacotes/cadastro', methods=['GET', 'POST'])
def cadastrarPacotes():
    form = PacoteForm ()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('cadastrarPacotes'))
    return render_template("cadastrarPacotes.html", form=form)


@app.route('/pacotes', methods=['GET', 'POST'])
@login_required
def pacotesLista():
    pesquisa = request.args.get('pesquisa', '')
    dados = Pacotes.query.order_by(Pacotes.id)  
    if pesquisa:
        dados = dados.filter(Pacotes.id.ilike(f"%{pesquisa}%"))
    context = {'dados': dados.all()}
    return render_template("pacotesLista.html", context=context)


@app.route('/turma/excluir/<int:id>', methods=['POST'])
@login_required
def delete(id):
    pacote = Pacotes.query.get_or_404(id)
    db.session.delete(pacote)
    db.session.commit()
    return redirect(url_for('homepage'))


@app.route('/pacote/edicao/<int:id>', methods=['GET', 'POST'])
def pacote(id):
    pacote = Pacotes.query.get_or_404(id)
    form = FechamentoForm(obj=pacote)

    if form.validate_on_submit():
        form.save()  

        
        pacote.disponibilidade = False
        db.session.commit()

        return redirect(url_for('homepage'))

    return render_template('pacote.html', form=form, pacote=pacote)

@app.route('/listapacote/', methods=['GET'])
@login_required
def listaPacote():
    pesquisa = request.args.get('pesquisa', '')

    dados = Fechamento.query.order_by(Fechamento.User_id)

    if pesquisa != '':
        dados = dados.filter(cast(Fechamento.User_id, String).ilike(f'%{pesquisa}%'))

    hoje = datetime.now()

    return render_template('listaPacote.html', dados=dados.all(), hoje=hoje)


@app.route('/cancelar/<int:id>', methods=['POST'])
def cancelar(id):
    fechamento = Fechamento.query.get_or_404(id)
    pacote = Pacotes.query.get(fechamento.Pacotes_id)

    if pacote:
        pacote.disponibilidade = True 

    db.session.delete(fechamento)  
    db.session.commit()

    return redirect(url_for('homepage'))