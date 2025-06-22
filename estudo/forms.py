from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_login import current_user
from estudo import db, bcrypt
from estudo.models import Lista, User 


class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')

    def validate_email(self, email):  # Corrigido aqui
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Usuário já cadastrado com esse email!')

    def save(self):
        senha_hash = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')  # Ajustado aqui
        user = User(
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            email=self.email.data,
            senha=senha_hash
        )
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data):
                return user
            else:
                raise Exception('Senha incorreta!')
        else:
            raise Exception('Usuário não encontrado!')


class ListaForm(FlaskForm):
    title = StringField('Título da tarefa', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self):
        if not current_user.is_authenticated:
            raise Exception("Usuário não autenticado!")

        lista = Lista(
            title=self.title.data,
            usuario=current_user  # ou: user_id=current_user.id
        )
        db.session.add(lista)
        db.session.commit()
        return lista