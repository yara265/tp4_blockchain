# web_api.py
from flask import Flask, request, jsonify
from flask_cors import CORS # Necessário para permitir requisições do frontend React
import app.app as bc_app # Importa sua lógica de negócio

app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas, permitindo que o React se comunique

# --- Rotas da API ---

@app.route('/api/users', methods=['GET'])
def get_users():
    """Retorna a lista de usuários e seus saldos."""
    # Retorna uma cópia para evitar modificar o dicionário original diretamente
    users_data = {username: {"saldo": data["saldo"]} for username, data in bc_app.users.items()}
    return jsonify(users_data)

@app.route('/api/register', methods=['POST'])
def register_user():
    """Cadastra um novo usuário."""
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({"success": False, "message": "Nome de usuário é obrigatório"}), 400

    # A senha está hardcoded como "123" na sua lógica original, não a passamos para bc_app.cadastrar_usuario
    if bc_app.cadastrar_usuario(username):
        return jsonify({"success": True, "message": f"Usuário {username} cadastrado com sucesso!"})
    else:
        return jsonify({"success": False, "message": f"Usuário {username} já existe."}), 409

@app.route('/api/transfer', methods=['POST'])
def transfer_funds():
    """Processa uma transferência de fundos."""
    data = request.get_json()
    sender = data.get('sender')
    recipient = data.get('recipient')
    value = data.get('value')

    if not all([sender, recipient, value]):
        return jsonify({"success": False, "message": "Dados de transferência incompletos."}), 400
    
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