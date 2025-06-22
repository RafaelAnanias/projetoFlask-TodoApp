from estudo import app, db
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required

from estudo.models import Lista
from estudo.forms import ListaForm, UserForm, LoginForm


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = form.login()  # Corrigido: agora chama a função corretamente
            login_user(user, remember=True)  # Faz login do usuário
            return redirect(url_for('listaTarefa'))  # Redireciona para a página com as tarefas
        except Exception as e:
            flash(str(e))  # Exibe mensagem de erro no template

    return render_template('index.html', form=form)


@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('listaTarefa'))  # Redireciona após cadastro
    return render_template('cadastro.html', form=form)


@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/lista/', methods=['GET', 'POST'])
@login_required
def novapag():
    form = ListaForm()

    if form.validate_on_submit():
        nova_lista = Lista(
            title=form.title.data,
            usuario=current_user  # Garante vínculo com o usuário logado
        )
        db.session.add(nova_lista)
        db.session.commit()
        return redirect(url_for('listaTarefa'))  # Redireciona para a lista de tarefas

    return render_template('lista.html', form=form)


@app.route('/lista/tarefa')
@login_required
def listaTarefa():
    pesquisa = request.args.get('pesquisa', '')

    dados = Lista.query.order_by(Lista.title)

    if pesquisa:
        dados = dados.filter(Lista.title.like(f"%{pesquisa}%"))

    dados = dados.all()

    context = {'dados': dados}

    return render_template('lista_tarefa.html', context=context)






















