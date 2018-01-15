# coding=utf-8
from configs import *
#from tabledef import Reserva
app = Flask(__name__)

#retorna os dados de todas as reservas
@app.route('/reservas', methods=['GET'])
def lista_reservas():
    engine = create_engine('sqlite:///tutorial.db', echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    b = s.query(User)
    query = engine.execute("select * from reservas") 
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
    result = {'data':[dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    #return result    
    #return 1
    return json.dumps(result)#[ row.username for row in b ])

#recebe dados para poder pedir ao servidor rpc para criar uma reserva
@app.route('/reservas', methods=['POST'])
def criar_reserva():
    POST_SALA_ID = int(request.form['sala_id'])
    POST_ID_USER = int(request.form['user_id'])#usamos este porque é o id de sessão
    POST_DIA_HORA = str(request.form['dia_hora'])
    proxy = xmlrpclib.ServerProxy("http://"+RPCSERVER+str(PORTA_RPCSERVER)+"/")
    if proxy.criar_reserva(POST_SALA_ID,POST_ID_USER,POST_DIA_HORA):
        return "reserva feita"
    else:
        return "erro na reserva"

#recebe um id de uma reserva e pede ao rpcserver para tornar o estado dessa reserva como pago
@app.route('/reservas/update', methods=['POST'])
def pagamento_reserva():
    POST_RESERVA_ID = str(request.form['id'])
    proxy = xmlrpclib.ServerProxy("http://"+RPCSERVER+str(PORTA_RPCSERVER)+"/")
    if proxy.pagamento_reserva(POST_RESERVA_ID):
        return "pagamento de reserva feita"
    else:
        return "erro no pagamento da reserva"

#retorna apenas uma reserva de acordo com o id forneceido
@app.route('/reservas/<int:id>', methods=['GET'])
def get_reserva(id):
    engine = create_engine(NOME_BASE_DADOS, echo=True)
    query = engine.execute("select * from reservas where reservas.id="+str(id)) 
    #Query the result and get cursor.Dumping that data to a JSON is looked by extension
    result = {'reservas': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return json.dumps(result)

#retorna todas as reservas com o id de sala fornecido
@app.route('/reservas/sala/<int:sala_id>', methods=['GET'])
def get_reserva_sala(sala_id):
    engine = create_engine(NOME_BASE_DADOS, echo=True)
    query = engine.execute("select * from reservas where reservas.sala_id="+str(sala_id)) 
    #Query the result and get cursor.Dumping that data to a JSON is looked by extension
    result = {'reservas': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return json.dumps(result)

#Retorna todas as reservas pertencentes ao utilizador 
@app.route('/reservas/user/<int:user_id>', methods=['GET'])
def get_reserva_user(user_id):
    engine = create_engine(NOME_BASE_DADOS, echo=True)
    query = engine.execute("select * from reservas where reservas.user_id="+str(user_id))
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return json.dumps(result)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=PORTA_RESERVAS)
