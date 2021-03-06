from flask import Flask, jsonify
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, update
from tabledef import *
import xmlrpclib
import json
from SimpleXMLRPCServer import SimpleXMLRPCServer
from configs import *

#connect bd
engine = create_engine('sqlite:///tutorial.db', echo=True)
Session = sessionmaker(bind=engine)
s = Session()

#autenticacao do utilizaodr. verifica se existe um utilizador na base de dados com o nome e pw fornecidos
def autenticar(user,pw):
    query = s.query(User).filter(User.username.in_([user]), User.password.in_([pw]) )
    result = query.first()
    if result:
        return True
    else:
        return False

#retorna o id de utilizador de acordo com o nome fornecido
def get_user_id(user):
    query = s.query(User).filter(User.username.in_([user]))
    result = query.first()
    if result:
        return result.id
    else:
        return 0

#retorna o saldo do utilizador
def get_user_saldo(user):
    query = s.query(User).filter(User.username.in_([user]))
    result = query.first()
    if result:
        return result.saldo
    else:
        return 0

#retorna as reservas
def get_reservas():
    b = s.query(Reserva.id, Reserva.dia_hora, Reserva.data_pagamento)
    a = []
    for row in b:
        a.append(row.id) 
    return a

#retorna apenas uma reserva
def get_reserva(id):
    b = s.query(Reserva).filter(Reserva.id.in_([id]))
    result = b.first()
    a = []
    a.append(result.id)
    a.append(result.dia_hora)
    a.append(result.data_pagamento)
    return a

#cria uma reserva
def criar_reserva(sala_id,cliente_id,dia_hora):
    #utilizando os modelos
    reserva = Reserva(dia_hora, sala_id, cliente_id)
    s.add(reserva)
    #conn = sqlite3.connect("tutorial.db")
    #c = conn.cursor()
    #c.execute('INSERT INTO reservas (dia_hora, sala_id, user_id) VALUES (%s, %s, %s)' % (dia_hora,sala_id,cliente_id))
    failed=False
    try:
        s.commit()
        #conn.commit()
    except Exception as e:
        failed=True
    if not failed:
        return True
    else:
        return False

#realiza o pagamento de uma reserva e introduz a data de pagamento (a data atual)
def pagamento_reserva(id_reserva):
    data_agora = datetime.now()
    data_agora_str = data_agora.strftime('%d-%m-%Y %H:%M:%S')
    s.query(Reserva).filter_by(id=id_reserva).update({"pagamento_feito":1})
    s.query(Reserva).filter_by(id=id_reserva).update({"data_pagamento":str(data_agora_str)})
    #conn = sqlite3.connect("tutorial.db")
    #c = conn.cursor()
    #c.execute("UPDATE reservas SET pagamento_feito = 1 WHERE id =%s" % id_reserva)
    #c.execute("UPDATE reservas SET data_pagamento = CURRENT_TIMESTAMP WHERE id =%s" % id_reserva)
    failed=False
    try:
        s.commit()
    except Exception as e:
        failed=True
    if not failed:
        return True
    else:
        return False

#atualiza o saldo de um utilizador
def update_saldo(valor,id_user):
    s.query(User).filter_by(id=id_user).update({"saldo":valor})
    #return True
    failed=False
    try:
        s.commit()
    except Exception as e:
        failed=True
    if not failed:
        return True
    else:
        return False

#cria uma sala
def criar_sala(nome_sala,preco_sala,capacidade_sala):
    sala = Sala(nome_sala, preco_sala, capacidade_sala)
    s.add(sala)
    failed=False
    try:
        s.commit()
    except Exception as e:
        failed=True
    if not failed:
        return True
    else:
        return False

#cria um utilizador
def criar_user(username, password, email, telefone):
    user = User(username, password, email, telefone)
    s.add(user)
    failed=False
    try:
        s.commit()
    except Exception as e:
        failed=True
    if not failed:
        return True
    else:
        return False
    
#definiçao do endereco do servidor
server = SimpleXMLRPCServer((SITE, PORTA_RPCSERVER), allow_none=true)
#registo de funcoes no servidor
server.register_function(autenticar, "autenticar")
server.register_function(get_reservas, "get_reservas")
server.register_function(get_reserva, "get_reserva")
server.register_function(criar_reserva, "criar_reserva")
server.register_function(pagamento_reserva, "pagamento_reserva")
server.register_function(get_user_id, "get_user_id")
server.register_function(get_user_saldo, "get_user_saldo")
server.register_function(criar_sala, "criar_sala")
server.register_function(criar_user, "criar_user")
server.register_function(update_saldo, "update_saldo")
#poe o servidor a correr infinitivamente
server.serve_forever()
