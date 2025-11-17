# web.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import app.app as bc_app  # Renomeando a importação para evitar conflitos

# Configuração do Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui' # Necessário para sessões/mensagens flash

# --- Rotas de Visualização (HTML) ---

@app.route('/')
def index():
    """Página principal: Cadastro e Login."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Painel de usuário: Visualização de saldo e Transferência."""
    # Como não temos um sistema de sessão robusto, vamos listar todos os usuários e a chain
    return render_template('dashboard.html', 
                           users=bc_app.users, 
                           blockchain=bc_app.blockchain.chain)

@app.route('/blockchain')
def view_chain():
    """Visualiza toda a cadeia de blocos em formato amigável."""
    # Para passar o objeto Block, você pode convertê-lo para um dicionário ou usar vars()
    chain_data = [vars(block) for block in bc_app.blockchain.chain]
    return render_template('blockchain.html', chain=chain_data)

# --- Rotas de Ação (API/Lógica) ---

@app.route('/register', methods=['POST'])
def register():
    """Processa o cadastro de novo usuário."""
    username = request.form.get('username')
    password = request.form.get('password') # Senha está hardcoded como '123' na lógica
    
    if not username:
        return redirect(url_for('index')) # Em uma app real, você enviaria um erro

    # Assumimos a senha "123" para o exemplo, ignorando o input password por simplicidade
    if bc_app.cadastrar_usuario(username):
        # Você pode usar flash() aqui para uma mensagem de sucesso
        print(f"Usuário {username} cadastrado com sucesso!")
    else:
        print(f"Erro ao cadastrar {username}.")
    
    return redirect(url_for('dashboard'))

@app.route('/transfer', methods=['POST'])
def transfer():
    """Processa a transferência de saldo entre usuários."""
    sender = request.form.get('sender')
    recipient = request.form.get('recipient')
    value = request.form.get('value')
    
    try:
        value = int(value)
    except ValueError:
        print("Valor inválido.")
        return redirect(url_for('dashboard'))

    if bc_app.transferir(sender, recipient, value):
        print(f"Transferência de {value} de {sender} para {recipient} realizada com sucesso!")
    else:
        print("Erro na transferência: saldo insuficiente ou usuário inexistente.")
        
    return redirect(url_for('dashboard'))

# --- Rota para API (Opcional) ---

@app.route('/api/chain', methods=['GET'])
def api_chain():
    """Retorna a blockchain em formato JSON."""
    chain_data = [vars(block) for block in bc_app.blockchain.chain]
    return jsonify(chain_data)

if __name__ == '__main__':
    # Inicializa alguns usuários para teste
    bc_app.cadastrar_usuario("Yara Nunes")
    bc_app.cadastrar_usuario("Carol")
    
    app.run(debug=True)