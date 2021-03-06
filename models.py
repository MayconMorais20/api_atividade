from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///atividades.db', convert_unicode = True)
db_session = scoped_session(sessionmaker(autocommit = False, bind = engine))

Base = declarative_base()
Base.query = db_session.query_property()

class quickcommit():
    def save(self):
        db_session.add(self)
        db_session.commit()
        
    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Pessoas(Base, quickcommit):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key = True)
    nome = Column(String(40), index = True)
    idade = Column(Integer)
    
    def __repr__(self):
        return '<Pessoa {}>'.format(self.nome)
    
class Usuarios(Base, quickcommit):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key = True)
    login = Column(String(80), unique = True)
    senha = Column(String(80))
    
    def __repre__(self):
        return '<Usuarios {}>'.format(self.login)    
      
class Atividades(Base,quickcommit):
    __tablename__ = 'atividades'
    id = Column(Integer, primary_key = True)
    nome = Column(String(80))
        
    #adicionando uma chave estrangeira
    pessoa_id = Column(Integer, ForeignKey("pessoas.id")) #Ex: ForeignKey("nome_tabela.id")
    pessoa = relationship("Pessoas") #Ex: relationship("Nome_da_classe")
        
    
def init_db():
    Base.metadata.create_all(bind = engine)
    
    
if __name__ == "__main__":
    init_db()