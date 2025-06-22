from estudo import app, db
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user, login_required

from estudo.models import Lista
from estudo.forms import ListaForm, UserForm, LoginForm


@app.route('/', methods=['GET', 'POST'])
def homepage():
    usuario = 'Rafael'
    form = LoginForm()

    if form.validate_on_submit():
        user = form.login 
        # login_user(user, remember=True)  # Se quiser ativar o login, descomente aqui

    context = {
        'usuario': usuario
    }

    return render_template('index.html', context=context, form=form)


@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)


@app.route('/sair/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/lista/', methods=['GET', 'POST'])
@login_required
def novapag():
    form = ListaForm()
    context = {}

    if form.validate_on_submit():
        nova_lista = Lista(
            title=form.title.data,
            usuario=current_user  # ou: user_id=current_user.id
        )
        db.session.add(nova_lista)
        db.session.commit()
        return redirect(url_for('homepage'))

    return render_template('lista.html', context=context, form=form)


@app.route('/lista/tarefa')
@login_required
def listaTarefa():
    pesquisa = request.args.get('pesquisa', '')

    dados = Lista.query.order_by(Lista.title)

    if pesquisa != '':
        dados = dados.filter(Lista.title.like(f"%{pesquisa}%"))

    dados = dados.all()

    context = {'dados': dados}

    return render_template('lista_tarefa.html', context=context)





























# from estudo import app, db
# from flask import render_template, url_for, request, redirect
# from flask_login import login_user, logout_user, current_user

# from estudo.models import Lista
# from estudo.forms import ListaForm, UserForm, LoginForm

# @app.route('/', methods = ['GET','POST' ]) 
# def homepage():
#     usuario = 'Rafael'
    
#     form = LoginForm()
    
#     if form.validate_on_submit():
#         user = form.login 
#         # login_user(user, remember=True)
    
    
    
#     context = {
#         'usuario': usuario
        
#     }
    
#     # print(current_user.is_authenticated)
 
#     return render_template('index.html', context=context, form=form)

# @app.route('/cadastro/', methods = ['GET','POST' ] )
# def cadastro():
#     form = UserForm()
#     if form.validate_on_submit():
#         user = form.save()
#         login_user(user, remember=True)
#         return redirect(url_for('homepage'))
#     return render_template('cadastro.html', form=form)

# @app.route('/sair/')
# def logout():
#     logout_user()
#     return redirect(url_for('homepage'))
    

# @app.route('/lista/', methods = ['GET','POST' ])
# def novapag():
#     form = ListaForm()
#     context = {}
#     if form.validate_on_submit():
#         form.save()
#         return redirect(url_for('homepage'))
        
#     return render_template('lista.html', context=context, form=form)
    
    
# @app.route('/lista/tarefa')
# def listaTarefa():
    
#     if request.method == 'GET':
#         pesquisa = request.args.get('pesquisa', '')
        
#         dados = Lista.query.order_by('title')
#         if pesquisa != '':
#             dados = dados.filter_by(title=pesquisa)
            
#             print(dados.all())
#             context = {'dados': dados.all()}
            
    
#     dados = Lista.query.order_by('title').all()
#     print(dados)
    

#     context = {'dados': dados }
    
    
    
    
    
#     return render_template('lista_tarefa.html', context=context)
    
