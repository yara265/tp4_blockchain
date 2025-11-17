# web_api.py
from flask import Flask, request, jsonify
from flask_cors import CORS # Necessário para permitir requisições do frontend React
import app.app as bc_app # Importa sua lógica de negócio

app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas, permitindo que o React se comunique

# --- Rotas da API ---

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Retorna a lista de usuários e seus saldos.
    Se logged_user for admin, retorna todos. Se for user, retorna apenas ele mesmo.
    """
    logged_user = request.args.get('logged_user')
    show_all = request.args.get('show_all', 'false').lower() == 'true'  # Para transferências
    
    if logged_user and bc_app.is_admin(logged_user):
        # Admin vê todos os usuários
        users_data = {username: {"saldo": data["saldo"], "role": data.get("role", "user")} 
                     for username, data in bc_app.users.items()}
    elif logged_user and show_all:
        # Usuário normal precisa ver todos para selecionar destinatário na transferência
        users_data = {username: {"saldo": data["saldo"], "role": data.get("role", "user")} 
                     for username, data in bc_app.users.items()}
    elif logged_user:
        # Usuário normal vê apenas seus dados
        user_data = bc_app.get_user_data(logged_user)
        if user_data:
            users_data = {logged_user: {"saldo": user_data["saldo"], "role": user_data.get("role", "user")}}
        else:
            users_data = {}
    else:
        # Sem login, retorna vazio
        users_data = {}
    
    return jsonify(users_data)

@app.route('/api/user/me', methods=['GET'])
def get_current_user():
    """Retorna dados do usuário logado."""
    username = request.args.get('username')
    if not username:
        return jsonify({"success": False, "message": "Usuário não especificado"}), 400
    
    user_data = bc_app.get_user_data(username)
    if user_data:
        return jsonify({
            "success": True,
            "username": user_data["username"],
            "saldo": user_data["saldo"],
            "role": user_data.get("role", "user")
        })
    else:
        return jsonify({"success": False, "message": "Usuário não encontrado"}), 404

@app.route('/api/register', methods=['POST'])
def register_user():
    """Cadastra um novo usuário. Apenas admin pode cadastrar."""
    data = request.get_json()
    username = data.get('username')
    logged_user = data.get('logged_user')  # Usuário que está fazendo o cadastro
    
    if not username:
        return jsonify({"success": False, "message": "Nome de usuário é obrigatório"}), 400
    
    # Verifica se o usuário logado é admin
    if logged_user and not bc_app.is_admin(logged_user):
        return jsonify({"success": False, "message": "Apenas administradores podem cadastrar usuários."}), 403

    # A senha está hardcoded como "123" na sua lógica original
    if bc_app.cadastrar_usuario(username, role="user"):
        return jsonify({"success": True, "message": f"Usuário {username} cadastrado com sucesso!"})
    else:
        return jsonify({"success": False, "message": f"Usuário {username} já existe."}), 409

@app.route('/api/login', methods=['POST'])
def login_user():
    """Autentica um usuário."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"success": False, "message": "Usuário e senha são obrigatórios"}), 400
    
    user_data = bc_app.login(username, password)
    if user_data:
        return jsonify({
            "success": True, 
            "message": f"Login realizado com sucesso!",
            "username": user_data["username"],
            "saldo": user_data["saldo"],
            "role": user_data.get("role", "user")
        })
    else:
        return jsonify({"success": False, "message": "Usuário ou senha incorretos"}), 401

@app.route('/api/transfer', methods=['POST'])
def transfer_funds():
    """Processa uma transferência de fundos."""
    data = request.get_json()
    sender = data.get('sender')
    recipient = data.get('recipient')
    value = data.get('value')
    logged_user = data.get('logged_user')  # Usuário logado

    if not all([sender, recipient, value]):
        return jsonify({"success": False, "message": "Dados de transferência incompletos."}), 400
    
    # Verifica se admin está envolvido na transferência (não pode ser remetente nem destinatário)
    if sender == "admin" or recipient == "admin":
        return jsonify({"success": False, "message": "O admin não pode ser remetente ou destinatário de transferências."}), 400
    
    # Verifica se o usuário logado pode fazer a transferência
    # Apenas o próprio usuário pode transferir (não admin transferindo por outros)
    if logged_user and not bc_app.is_admin(logged_user):
        if logged_user != sender:
            return jsonify({"success": False, "message": "Você só pode fazer transferências da sua própria conta."}), 403
    
    try:
        value = int(value)
        if value <= 0:
            raise ValueError("Valor deve ser positivo.")
    except ValueError:
        return jsonify({"success": False, "message": "Valor inválido."}), 400

    if bc_app.transferir(sender, recipient, value):
        return jsonify({"success": True, "message": "Transferência realizada com sucesso!"})
    else:
        return jsonify({"success": False, "message": "Erro na transferência: saldo insuficiente ou usuário inexistente."}), 400

@app.route('/api/blockchain', methods=['GET'])
def get_blockchain():
    """Retorna toda a cadeia de blocos."""
    # Converte os objetos Block para dicionários para serialização JSON
    chain_data = []
    for block in bc_app.blockchain.chain:
        block_dict = vars(block).copy()
        # Converte timestamp para um formato legível, se desejar
        block_dict['timestamp'] = int(block_dict['timestamp']) 
        chain_data.append(block_dict)
    return jsonify(chain_data)

if __name__ == '__main__':
    # Garante que Flask-CORS esteja instalado
    # pip install Flask-Cors
    app.run(debug=True, port=5001)