# coding=utf-8
NOME_BASE_DADOS = 'sqlite:///tutorial.db'
ENDERECO = 'http://127.0.0.1'
SITE = '0.0.0.0'
#Portas dos varios servicos
PORTA_ROTAS = 4003
PORTA_RESERVAS = 4001
PORTA_SALAS = 4002
PORTA_RPCSERVER = 8000
#utilizado nos containers
SALAS = 'salas:'
RESERVAS = 'reservas:'
ROTAS = 'rotas:'
RPCSERVER = 'rpcserver:'
ENDERECOS_PORTAS = [ROTAS, str(PORTA_ROTAS), RESERVAS,str(PORTA_RESERVAS), SALAS, str(PORTA_SALAS), RPCSERVER, str(PORTA_RPCSERVER)]
MENSAGEM_LOGIN_FIRST = "<p>Por favor faca login primeiro</p>"
from flask import Flask,jsonify
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import Flask, make_response, flash, redirect, render_template, request, session, abort
import os
from tabledef import *
import xmlrpclib
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float, Time, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from SimpleXMLRPCServer import SimpleXMLRPCServer
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
import requests
import json
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
from sqlalchemy import func, update
import csv
from flask_bootstrap import Bootstrap
#from flask_login import current_user
