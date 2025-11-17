from blockchain.blockchain import Blockchain

users = {}
blockchain = Blockchain()

def cadastrar_usuario(username):
    if username in users:
        return False
    users[username] = {"senha":"123", "saldo":10}
    # Cria um bloco para registrar o cadastro do usuário e o saldo inicial
    blockchain.add_block({
        "tipo": "cadastro",
        "usuario": username,
        "saldo_inicial": 10
    })
    return True

def login(username, senha):
    return username in users and users[username]["senha"] == senha

def transferir(de, para, valor):
    if de not in users or para not in users:
        return False
    if users[de]["saldo"] < valor:
        return False
    users[de]["saldo"] -= valor
    users[para]["saldo"] += valor
    # Cria um bloco para registrar a transferência
    blockchain.add_block({
        "tipo": "transferencia",
        "de": de,
        "para": para,
        "valor": valor
    })
    return True
