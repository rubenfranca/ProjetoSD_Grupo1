from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float, Time, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    saldo = Column(Float)
    email = Column(String)
    telefone = Column(String)
    reservas = relationship('Reserva')#, backref='user', lazy=True)
 
    #----------------------------------------------------------------------
    def __init__(self, username, password, email, telefone):
        """"""
        self.username = username
        self.password = password
        self.saldo = 0
        self.email = email
        self.telefone = telefone
 
class Sala(Base):
    __tablename__ = "salas"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    preco = Column(Float)
    capacidade = Column(Integer)
    
    reservas = relationship('Reserva')#, backref='sala', lazy=True)
    
    def __init__(self, nome, preco, capacidade):
        self.nome = nome
        self.preco = preco
        self.capacidade = capacidade

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True)
    dia_hora = Column(String(20))
    data_pagamento = Column(String, nullable = true)
    pagamento_feito = Column(Integer)
    sala_id = Column(Integer, ForeignKey('salas.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    def __init__(self, dia_hora, sala_id, user_id):
        self.dia_hora = dia_hora
        self.data_pagamento = '0'
        self.pagamento_feito = 0
        self.sala_id = sala_id
        self.user_id = user_id
    
    @property
    def serialize(self):
        return{
            'id': self.id,
            'dia_hora': self.dia_hora
            }
            

