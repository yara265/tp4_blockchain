import hashlib, time, json

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        raw = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def mine_block(self, difficulty):
        """
        Minera o bloco encontrando um hash que comece com 'difficulty' zeros.
        """
        target = "0" * difficulty  # Ex: se difficulty=4, target = "0000"
        start_time = time.time()
        last_log_time = start_time
        log_interval = 2.0  # Log a cada 2 segundos
        attempts = 0
        
        print(f"  🎯 Alvo: hash deve começar com '{target}'")
        print(f"  🔄 Iniciando mineração...")
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            attempts += 1
            self.hash = self.calculate_hash()
            
            # Log de progresso a cada intervalo
            current_time = time.time()
            if current_time - last_log_time >= log_interval:
                elapsed = current_time - start_time
                hashes_per_sec = attempts / elapsed if elapsed > 0 else 0
                print(f"  ⏳ Tentativa {attempts:,} | Nonce: {self.nonce:,} | "
                      f"{hashes_per_sec:,.0f} hashes/seg | Hash atual: {self.hash[:20]}...")
                last_log_time = current_time
        
        total_time = time.time() - start_time
        hashes_per_sec = attempts / total_time if total_time > 0 else 0
        
        print(f"  ✅ Hash válido encontrado!")
        print(f"  📊 Estatísticas:")
        print(f"     • Tentativas: {attempts:,}")
        print(f"     • Nonce final: {self.nonce:,}")
        print(f"     • Tempo total: {total_time:.2f} segundos")
        print(f"     • Velocidade: {hashes_per_sec:,.0f} hashes/segundo")
        
        return self.hash

class Blockchain:
    def __init__(self, difficulty=4):
        """
        Inicializa o blockchain com uma dificuldade configurável.
        difficulty: número de zeros que o hash deve começar (padrão: 4)
        """
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        print("\n" + "="*60)
        print("🏗️  CRIANDO BLOCO GENESIS")
        print("="*60)
        genesis = Block(0, time.time(), {"msg":"Genesis"}, "0")
        genesis.mine_block(self.difficulty)
        print(f"  🔗 Hash: {genesis.hash}")
        print(f"  📅 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(genesis.timestamp))}")
        print("="*60 + "\n")
        return genesis

    def add_block(self, data):
        """
        Adiciona um novo bloco à cadeia, minerando-o primeiro.
        """
        last = self.chain[-1]
        new = Block(len(self.chain), time.time(), data, last.hash)
        
        print("\n" + "="*60)
        print(f"⛏️  MINERANDO BLOCO #{new.index}")
        print("="*60)
        print(f"  📦 Dados do bloco:")
        print(f"     {json.dumps(data, indent=6, ensure_ascii=False)}")
        print(f"  🔗 Hash do bloco anterior: {last.hash[:40]}...")
        
        start_time = time.time()
        new.mine_block(self.difficulty)
        mining_time = time.time() - start_time
        
        print(f"\n  🎉 BLOCO #{new.index} MINERADO COM SUCESSO!")
        print(f"  📋 Detalhes do bloco:")
        print(f"     • Hash: {new.hash}")
        print(f"     • Nonce: {new.nonce:,}")
        print(f"     • Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(new.timestamp))}")
        print(f"     • Hash anterior: {new.previous_hash[:40]}...")
        print(f"  ⏱️  Tempo total de mineração: {mining_time:.2f} segundos")
        
        print(f"\n  ➕ Adicionando bloco #{new.index} à cadeia...")
        self.chain.append(new)
        print(f"  ✅ Bloco #{new.index} adicionado! Cadeia agora tem {len(self.chain)} blocos")
        print("="*60 + "\n")
        
        return new
    
    def is_valid(self):
        """
        Valida a integridade da cadeia de blocos.
        Verifica se todos os hashes são válidos e se a cadeia está conectada corretamente.
        """
        print("\n" + "="*60)
        print("🔍 VALIDANDO CADEIA DE BLOCOS")
        print("="*60)
        
        if len(self.chain) == 0:
            print("  ❌ Cadeia vazia!")
            print("="*60 + "\n")
            return False
        
        # Valida o bloco genesis
        print(f"\n  📋 Validando bloco Genesis (#0)...")
        genesis = self.chain[0]
        if genesis.index != 0:
            print(f"  ❌ Bloco Genesis tem index incorreto: {genesis.index}")
            print("="*60 + "\n")
            return False
        
        if genesis.previous_hash != "0":
            print(f"  ❌ Bloco Genesis tem previous_hash incorreto: {genesis.previous_hash}")
            print("="*60 + "\n")
            return False
        
        # Verifica se o hash do genesis é válido (começa com zeros)
        if genesis.hash[:self.difficulty] != "0" * self.difficulty:
            print(f"  ❌ Hash do Genesis não atende à dificuldade (deve começar com {self.difficulty} zeros)")
            print(f"     Hash: {genesis.hash}")
            print("="*60 + "\n")
            return False
        
        # Verifica se o hash calculado corresponde ao hash armazenado
        calculated_hash = genesis.calculate_hash()
        if genesis.hash != calculated_hash:
            print(f"  ❌ Hash do Genesis não corresponde ao hash calculado!")
            print(f"     Hash armazenado: {genesis.hash}")
            print(f"     Hash calculado: {calculated_hash}")
            print("="*60 + "\n")
            return False
        
        print(f"  ✅ Bloco Genesis válido")
        print(f"     Hash: {genesis.hash}")
        
        # Valida os blocos subsequentes
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            print(f"\n  📋 Validando bloco #{current.index}...")
            
            # Verifica se o index está correto
            if current.index != i:
                print(f"  ❌ Index incorreto! Esperado: {i}, Encontrado: {current.index}")
                print("="*60 + "\n")
                return False
            
            # Verifica se o previous_hash está correto
            if current.previous_hash != previous.hash:
                print(f"  ❌ Previous hash não corresponde ao hash do bloco anterior!")
                print(f"     Esperado: {previous.hash}")
                print(f"     Encontrado: {current.previous_hash}")
                print("="*60 + "\n")
                return False
            
            # Verifica se o hash atende à dificuldade
            if current.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"  ❌ Hash não atende à dificuldade (deve começar com {self.difficulty} zeros)")
                print(f"     Hash: {current.hash}")
                print("="*60 + "\n")
                return False
            
            # Verifica se o hash calculado corresponde ao hash armazenado
            calculated_hash = current.calculate_hash()
            if current.hash != calculated_hash:
                print(f"  ❌ Hash não corresponde ao hash calculado!")
                print(f"     Hash armazenado: {current.hash}")
                print(f"     Hash calculado: {calculated_hash}")
                print("="*60 + "\n")
                return False
            
            print(f"  ✅ Bloco #{current.index} válido")
            print(f"     Hash: {current.hash}")
            print(f"     Conectado ao bloco anterior: ✅")
        
        print(f"\n  🎉 CADEIA VÁLIDA!")
        print(f"  📊 Resumo:")
        print(f"     • Total de blocos: {len(self.chain)}")
        print(f"     • Dificuldade: {self.difficulty}")
        print(f"     • Todos os hashes são válidos: ✅")
        print(f"     • Cadeia está conectada corretamente: ✅")
        print("="*60 + "\n")
        
        return True
