#!/usr/bin/env python3
"""
Script de teste para demonstrar que o cadastro de usuário cria um bloco.
"""

import app.app as bc_app

def test_cadastro():
    print("=" * 60)
    print("TESTE: CADASTRO DE USUÁRIO CRIA BLOCO")
    print("=" * 60)
    
    # Limpa o blockchain para teste (em produção não faria isso)
    bc_app.blockchain = bc_app.blockchain.__class__(difficulty=4)
    bc_app.users = {}
    
    print("\n1. Cadastrando usuário 'alice'...")
    bc_app.cadastrar_usuario("alice")
    
    print("\n2. Cadastrando usuário 'bob'...")
    bc_app.cadastrar_usuario("bob")
    
    print("\n3. Verificando a cadeia de blocos:")
    print(f"   Total de blocos: {len(bc_app.blockchain.chain)}")
    print("\n   Blocos na cadeia:")
    for i, block in enumerate(bc_app.blockchain.chain):
        print(f"\n   Bloco #{i}:")
        print(f"     Tipo: {block.data.get('tipo', 'genesis')}")
        if block.data.get('tipo') == 'cadastro':
            print(f"     Usuário: {block.data.get('usuario')}")
            print(f"     Saldo inicial: {block.data.get('saldo_inicial')}")
        elif block.data.get('tipo') == 'transferencia':
            print(f"     De: {block.data.get('de')}")
            print(f"     Para: {block.data.get('para')}")
            print(f"     Valor: {block.data.get('valor')}")
        print(f"     Hash: {block.hash[:40]}...")
    
    print("\n" + "=" * 60)
    print("✅ Teste concluído!")
    print("=" * 60)

if __name__ == "__main__":
    test_cadastro()

