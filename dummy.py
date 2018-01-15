#ficheiro utilizado para meter dados na base de dados

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
from datetime import datetime
from tabledef import *
from sqlalchemy import Column, Date, Integer, String, Float, Time, Boolean
import sqlite3
import atualizar_tabela
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("admin","password", "emailad", "291")
session.add(user)
 
user = User("python","python", "emailp", "292")
session.add(user)

user = User("123","123", "email123", "123123")
session.add(user)

t = datetime.now()
reserva = Reserva(t.strftime('21/%m/%Y'),1,1)
session.add(reserva)

sala = Sala("sala 23",20,30)
session.add(sala)

sala = Sala("sala 15",43,50)
session.add(sala)
 
# commit the record the database
session.commit()
 
session.commit()
