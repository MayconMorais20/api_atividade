from models import Pessoas


#insere dados na tabela pessoa  
def insere_pessoas():
    pessoa = Pessoas(nome = 'Mario', idade = 24)
    print(pessoa)
    pessoa.save()
    
#consulta dados na tabela pessoa  
def consulta():
    pessoas = Pessoas.query.filter_by(nome = 'Rafael')
    for pessoa in pessoas:
        print(f'nome: {pessoa.nome}, idade: {pessoa.idade}.')

#retorna 'todos' os dados na tabela pessoa  
def find_all(safequery=True):
    #limitado a 10 linha, sendo necessario implicitar caso retornar todos os dados
    pessoas = Pessoas.query.all()
    count = 0
    for pessoa in pessoas:
        print(f'nome: {pessoa.nome}, idade: {pessoa.idade}.')
        if safequery:
            count += 1
            if count == 10:
                break

#altera dados na tabela pessoa  
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome = 'Galleani').first()
    pessoa.idade = 44
    pessoa.save()
    
#exclui dados na tabela pessoa  
def excluir_pessoa():
    pessoa = Pessoas.query.filter_by(nome = 'Rafael').first()
    pessoa.delete()
    
if __name__ == "__main__":
    insere_pessoas()
    #consulta()
    find_all()
    