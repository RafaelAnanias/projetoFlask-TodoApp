from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError#EqualTo Verifica se uma senha está igual a outra
from estudo import db, bcrypt
from estudo.models import Lista, User 


class UserForm(FlaskForm):
          nome = StringField('Nome', validators=[DataRequired()])
          sobrenome = StringField('Sobrenome', validators=[DataRequired()])
          email = StringField('E-mail', validators=[DataRequired()])
          senha = PasswordField('Senha', validators=[DataRequired()])
          confirmacao_senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('senha')])
          btnSubmit = SubmitField('Cadastrar')
          
          def validade_email(self, email):
               if User.query.filter(email=email.data).first():
                    return ValidationError('Usuário já cadastrado com esse email!!!')
               
                
          def save(self):
               senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
               user = User (
                    nome = self.nome.data,
                    sobrenome = self.sobrenome.data,
                    email = self.email.data,
                    senha = senha
                    
               )
               
               db.session.add (user)
               db.session.commit()
               return user
               
          
          
      



class LoginForm(FlaskForm):
      email = StringField('E-mail', validators=[DataRequired()])
      senha = PasswordField('Senha', validators=[DataRequired()])
      btnSubmit = SubmitField('Login')
      
      def login(self):
           #Recuperar o usuário do e-mail
           user = User.query.filter_by(email=self.email.data).first()
           
           #Verificar se a senha é válida
           
           if user:
                if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                     #Retorna o usuário
                     return user
                else: raise Exception ('Senha incorreta!!!')
           else:
               raise Exception ('Usuário não encontrado!!!')

     

class ListaForm(FlaskForm):
     title = StringField('Título da tarefa', validators=[DataRequired()])
     btnSubmit = SubmitField('Enviar')
     
     def save(self):
          lista = Lista (
               title = self.title.data
          )
          db.session.add(lista)
          db.session.commit()
          