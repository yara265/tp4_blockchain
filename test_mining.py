#!/usr/bin/env python3
"""
Script de teste para demonstrar a mineração (Proof of Work) no blockchain.
"""

from blockchain.blockchain import Blockchain
import time

def test_mining():
    print("=" * 60)
    print("TESTE DE MINERAÇÃO (PROOF OF WORK)")
    print("=" * 60)
    
    # Cria um blockchain com dificuldade 4 (hash deve começar com 4 zeros)
    print("\n1. Criando blockchain com dificuldade 4...")
    blockchain = Blockchain(difficulty=4)
    
    print(f"\n2. Bloco Genesis criado e minerado:")
    genesis = blockchain.chain[0]
    print(f"   Hash: {genesis.hash}")
    print(f"   Nonce: {genesis.nonce}")
    print(f"   Hash começa com 4 zeros? {genesis.hash.startswith('0000')}")
    
    # Adiciona alguns blocos para demonstrar a mineração
    print("\n3. Adicionando blocos com transferências...")
    
    for i in range(3):
        print(f"\n--- Adicionando bloco {i+1} ---")
        data = {
            "de": f"usuario{i}",
            "para": f"usuario{i+1}",
            "valor": 10 * (i+1)
        }
        block = blockchain.add_block(data)
        print(f"   Dados: {data}")
        print(f"   Hash válido? {block.hash.startswith('0' * blockchain.difficulty)}")
    
    print("\n" + "=" * 60)
    print("RESUMO DA CADEIA:")
    print("=" * 60)
    for block in blockchain.chain:
        print(f"\nBloco {block.index}:")
        print(f"  Hash: {block.hash}")
        print(f"  Nonce: {block.nonce}")
        print(f"  Dados: {block.data}")
        print(f"  Hash anterior: {block.previous_hash[:20]}...")
    
    # Testa a validação da cadeia
    print("\n" + "=" * 60)
    print("TESTANDO VALIDAÇÃO DA CADEIA")
    print("=" * 60)
    blockchain.is_valid()

if __name__ == "__main__":
    test_mining()

