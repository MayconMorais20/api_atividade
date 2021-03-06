from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from models import Pessoas, Atividades, Usuarios

auth = HTTPBasicAuth()
app  = Flask(__name__)
api  = Api(app)

#USUARIOS = {
    #'root': 'root123',
    #'maycon':'Adm@Adm'
#}

@auth.verify_password
def veirificacao(login, senha):
    if not (login, senha):
        return True
    return Usuarios.query.filter_by(login= login, senha = senha).first()
        
class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome = nome).first()
        try:
            response = {
                'nome': pessoa.nome,    
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'registro nao encontrado'
            }
        return response
    @auth.login_required
    def put(self,nome):
        pessoa = Pessoas.query.filter_by(nome = nome).first()
        dado = request.json
        if 'nome' in dado:
            pessoa.nome = dado['nome']
        if 'idade' in  dado:
            pessoa.idade = dado['idade']    
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response
    @auth.login_required
    def delete(self,nome):
        pessoa = Pessoas.query.filter_by(nome = nome ).first()
        mensagem = f'A pessoa {pessoa.nome}, foi excluida.'
        pessoa.delete()
        return {
            'status': 'sucesso',
            'mensagem': mensagem
        }

class ListaPessoas(Resource):
    
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': pessoa.id,'nome': pessoa.nome,'idade': pessoa.idade} for pessoa in pessoas] 
        
        return response
    
    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome= dados['nome'],idade = dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        
        return response

class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        return [{'id':atividade.id ,
                 'nome': atividade.nome, 
                 'pessoa': atividade.pessoa.nome
                 
                } for atividade in atividades]
    
    def post(self):
        dado = request.json
        pessoa = Pessoas.query.filter_by(nome = dado['pessoa']).first()
        atividade = Atividades(nome = dado['nome'], pessoa = pessoa)
        atividade.save()
        response = {
            'pessoa' : atividade.pessoa.nome,
            'nome' : atividade.nome,
            'id' : atividade.id
        }

        return response

class Home(Resource):
    def get(self):
        return '** HOME **'
    
api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(Home, '/')
    
if __name__ == "__main__":
    app.run(debug = True)