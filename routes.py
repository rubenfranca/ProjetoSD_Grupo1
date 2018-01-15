# coding=utf-8
from configs import *
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
app = Flask(__name__)

#home() é reutilizado para decidir se o user esta com login ou nao
@app.route('/')
def home():
    if not session.get('logged_in'):
        #render_template mostra no ecra o conteudo de login.html
        return render_template('login.html')
    else:
        #é passada a variavel saldo que é utilizada no ficheiro home.html
        return render_template('home.html', saldo=session['saldo'])

      
@app.route('/login', methods=['GET'])
def do_admin_login_get():
    return home()

#autenticação do utilizador 
@app.route('/login', methods=['POST'])
def do_admin_login():
    #busca de username e password do formulario
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    #comunicaçao com rpcserver
    proxy = xmlrpclib.ServerProxy("http://"+RPCSERVER+str(PORTA_RPCSERVER)+"/")
    #session['logged_in'] fica com true ou false se o user esta autenticado ou nao
    session['logged_in'] = proxy.autenticar(POST_USERNAME, POST_PASSWORD)
    #busca o id do utilizador de acordo com o nome de utilizador
    session['user_id'] = proxy.get_user_id(POST_USERNAME)
    session['username'] = POST_USERNAME
    #busca o saldo do utilizador
    session['saldo'] = proxy.get_user_saldo(POST_USERNAME)
    return home()
 
@app.route("/logout")
def logout():
    #logout do utilizador
    session['logged_in'] = False
    return home()

#mostra as reservas do utilizador autenticado
@app.route("/reservas")
def reservas():
    if not session.get('logged_in'):
        return render_template('login.html', mensagem=MENSAGEM_LOGIN_FIRST, rotas=PORTA_ROTAS)
    else:
        #pedido ao serviço de reservas para mostrar as reservas do utilizador
        r = requests.get("http://"+RESERVAS+str(PORTA_RESERVAS)+"/reservas/user/"+str(session['user_id']))
        #pede ao serviço de salas todas as salas
        s = requests.get("http://"+SALAS+str(PORTA_SALAS)+"/salas")
        #conversão para json
        a =r.json()
        b = s.json()
        #max = numero de reservas do utilizador
        max = len(a['data'])
        #html que ira ser enviado para o ecra com as reservas por pagar
        html ="<p>Reservas por Pagar:</p><p></p><table class='table table-dark table-hover'><thead><tr><td>Identificacao da reserva</td><td>Sala</td><td>Dia e Hora da Reserva</td></tr></thead><tbody>"
        #mostra os dados de cada reserva
        for i in range(0,max):
            if a['data'][i]['pagamento_feito'] == 0:
                id_sala = a['data'][i]['sala_id']
                html += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" %(a['data'][i]['id'],b['data'][id_sala-1]['nome'],a['data'][i]['dia_hora'])   
        html += "</tbody></table>"
        #mostra as reservas pagas
        html +="<p>Reservas Pagas:</p><p></p><table class='table table-dark table-hover'><thead><tr><td>Identificacao da reserva</td><td>Sala</td><td>Dia e Hora da Reserva</td><td>Data do Pagamento</td></tr></thead><tbody>"
        for i in range(0,max):
            if a['data'][i]['pagamento_feito'] == 1:
                id_sala = a['data'][i]['sala_id']
                html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %(a['data'][i]['id'],b['data'][id_sala-1]['nome'],a['data'][i]['dia_hora'],a['data'][i]['data_pagamento'])   
        html+= "</tbody></table>"
        
        return render_template('reservas.html', dados=html)

#criar_reserva mostra todas as salas e apresenta um formulario para criar uma reserva
@app.route("/criarReserva", methods=['GET'])
def criar_reserva():
    if not session.get('logged_in'):
        return render_template('login.html', mensagem=MENSAGEM_LOGIN_FIRST)
    else:
        #pede ao serviço salas todas as salas
        r = requests.get("http://"+SALAS+str(PORTA_SALAS)+"/salas")
        #tabela_sala mostra todas as salas
        tabela_sala ="<table class='table table-dark table-hover'>"\
               "<thead><tr><td>nome</td><td>preco</td><td>capacidade</td></tr></thead><tbody>"
        a =r.json()
        max = len(a['data'])
        for i in range(0,max):
            tabela_sala += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" %(a['data'][i]['nome'],a['data'][i]['preco'],a['data'][i]['capacidade'])   
        tabela_sala+= "</tbody></table>"
        #select no formulario com o nome das salas
        dropdown_sala = "<select class='form-control' name='sala_id'>"
        for i in range(0,max):
            dropdown_sala += "<option value=%s>%s</option>" %(a['data'][i]['id'],a['data'][i]['nome'])
        dropdown_sala += "</select>"      
        return render_template('criarReserva.html', tabela_salas=tabela_sala, dropdown_salas=dropdown_sala)

#recebe os dados do formulario
@app.route("/criarReserva", methods=['POST'])
def criar_reserva_post():
    POST_SALA_ID = int(request.form['sala_id'])
    POST_DIA = str(request.form['dia'])
    POST_HORA = str(request.form['hora'])
    POST_DIA_HORA = POST_HORA+" "+POST_DIA
    #servico reservas trata de fazer a criação de reserva
    r = requests.post("http://"+RESERVAS+str(PORTA_RESERVAS)+"/reservas", data= {'sala_id':POST_SALA_ID,'dia_hora':POST_DIA_HORA, 'user_id':session['user_id']})
    return home()

#mostra as reservas por pagar e permite ao utilizador escolher quais a quer pagar
@app.route("/pagarReserva", methods=['GET'])
def pagar_reserva_get():
    if not session.get('logged_in'):
        return render_template('login.html', mensagem=MENSAGEM_LOGIN_FIRST)
    else:
        r = requests.get("http://"+RESERVAS+str(PORTA_RESERVAS)+"/reservas/user/"+str(session['user_id']))
        s = requests.get("http://"+SALAS+str(PORTA_SALAS)+"/salas")
        b = s.json()
        html ="<table class='table table-dark table-hover'><thead><tr><td>Identificacao da reserva</td><td>Dia e Hora da Reserva</td><td>Sala</td><td>Preco da Reserva</td><td>Pagar</td></tr></thead><tbody>"
        a =r.json()
        max = len(a['data'])
        for i in range(0,max):
            if a['data'][i]['pagamento_feito'] == 0:
                id_sala = a['data'][i]['sala_id']
                html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><input type='checkbox' name='pagamentos' value='%s'></td></tr>" %(a['data'][i]['id'],a['data'][i]['dia_hora'],b['data'][id_sala-1]['nome'],b['data'][id_sala-1]['preco'],a['data'][i]['id'])   
        html+= "</tbody></table>"
        return render_template('pagarReservas.html', dados=html)

#recebe as reservas que o utilizador quer pagar e se tem saldo suficiente para pagar todas, é efetuada a transação.
@app.route("/pagarReserva", methods=['POST'])
def pagar_reserva_post():
    POST_RESERVAS_ID = request.form.getlist('pagamentos')
    tam = len(POST_RESERVAS_ID)
    r = requests.get("http://"+RESERVAS+str(PORTA_RESERVAS)+"/reservas")
    s = requests.get("http://"+SALAS+str(PORTA_SALAS)+"/salas")
    a =r.json()
    b = s.json()
    total = 0
    for i in range(0,tam):
        id_sala = a['data'][int(POST_RESERVAS_ID[i])-1]['sala_id']
        total = total + b['data'][id_sala-1]['preco']
    if session['saldo'] >= total:    
        for i in range(0,tam):
            r = requests.post("http://"+RESERVAS+str(PORTA_RESERVAS)+"/reservas/update", data= {'id':POST_RESERVAS_ID[i]})
        proxy = xmlrpclib.ServerProxy("http://"+RPCSERVER+str(PORTA_RPCSERVER)+"/")
        valor = int(session ['saldo'])- int(total)
        if proxy.update_saldo(valor,session['user_id']):
            session['saldo'] -= int(total) 
        return home()
    else:
        return "nao ha dinheiro"+home()

#recebe a quantidade de saldo a adicionar na conta
@app.route("/adicionarSaldo", methods=['POST'])
def update_saldo():
    POST_QUANTIDADE_SALDO = request.form['quantidade']
    proxy = xmlrpclib.ServerProxy("http://"+RPCSERVER+str(PORTA_RPCSERVER)+"/")
    valor = int(session['saldo'])+int(POST_QUANTIDADE_SALDO)
    if proxy.update_saldo(valor,session['user_id']):
        session['saldo'] += int(POST_QUANTIDADE_SALDO) 
        return home()
    else:
        return "erro ao adicionar saldo"

#recebe dados para criar um utilizador
@app.route('/criarUser', methods=['POST'])
def criar_user():
    username, password, email, telefone
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    POST_EMAIL = str(request.form['email'])
    POST_TELEFONE = int(request.form['telefone'])
    proxy = xmlrpclib.ServerProxy("http://"+RPCSERVER+str(PORTA_RPCSERVER)+"/")
    if proxy.criar_user(POST_USERNAME, POST_PASSWORD, POST_EMAIL,POST_TELEFONE):
        return "utilizador criado"
    else:
        return "erro ao criar utilizador"

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=PORTA_ROTAS)
