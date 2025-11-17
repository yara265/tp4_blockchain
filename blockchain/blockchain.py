import hashlib, time, json

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        raw = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.previous_hash}"
        return hashlib.sha256(raw.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"msg":"Genesis"}, "0")

    def add_block(self, data):
        last = self.chain[-1]
        new = Block(len(self.chain), time.time(), data, last.hash)
        self.chain.append(new)
        return new
