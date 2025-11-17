from blockchain.blockchain import Blockchain

users = {}
blockchain = Blockchain()

# Cria usuário admin inicial
def init_admin():
    """Inicializa o usuário admin se não existir."""
    if "admin" not in users:
        users["admin"] = {"senha": "admin123", "saldo": 0, "role": "admin"}
        blockchain.add_block({
            "tipo": "cadastro",
            "usuario": "admin",
            "saldo_inicial": 0,
            "role": "admin"
        })

# Inicializa admin ao importar o módulo
init_admin()

def cadastrar_usuario(username, role="user"):
    """
    Cadastra um novo usuário.
    role: "admin" ou "user" (padrão: "user")
    """
    if username in users:
        return False
    users[username] = {"senha":"123", "saldo":10, "role": role}
    # Cria um bloco para registrar o cadastro do usuário e o saldo inicial
    blockchain.add_block({
        "tipo": "cadastro",
        "usuario": username,
        "saldo_inicial": 10,
        "role": role
    })
    return True

def login(username, senha):
    """
    Autentica um usuário e retorna informações dele.
    Retorna dict com user info ou None se falhar.
    """
    if username in users and users[username]["senha"] == senha:
        user = users[username].copy()
        user["username"] = username
        return user
    return None

def is_admin(username):
    """Verifica se o usuário é admin."""
    return username in users and users[username].get("role") == "admin"

def get_user_data(username):
    """Retorna dados do usuário."""
    if username in users:
        user = users[username].copy()
        user["username"] = username
        return user
    return None

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
