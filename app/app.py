from blockchain.blockchain import Blockchain

users = {}
blockchain = Blockchain()

def cadastrar_usuario(username):
    if username in users:
        return False
    users[username] = {"senha":"123", "saldo":10}
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
    blockchain.add_block({"de":de,"para":para,"valor":valor})
    return True
