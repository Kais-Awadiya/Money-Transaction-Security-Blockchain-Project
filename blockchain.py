import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash, difficulty=4):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.difficulty = difficulty  # Difficulty of the mining
        self.hash = None
        self.nonce = 0  # Used to find the correct hash
        self.mine_block()  # Start mining the block

    def calculate_hash(self):
        # Concatenate all block data and apply SHA-256 hash
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        # Keep iterating until we find a hash that meets the difficulty target
        while self.calculate_hash()[:self.difficulty] != "0" * self.difficulty:
            self.nonce += 1  # Increment the nonce
        self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")


class Blockchain:
    def __init__(self):
        # Initialize the chain with the genesis (first) block
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Manually create the first block in the chain (index 0)
        genesis_block = Block(0, time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        # Add a new block with the given data
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time(), data, previous_block.hash)
        self.chain.append(new_block)
        return new_block



# # Test code to check the blockchain functionality and PoW

# blockchain = Blockchain()

# # Add some blocks with transactions
# blockchain.add_block({"sender": "Alice", "receiver": "Bob", "amount": 100})
# blockchain.add_block({"sender": "Bob", "receiver": "Charlie", "amount": 50})

# # Print out all blocks in the blockchain
# for block in blockchain.chain:
#     print(f"Block #{block.index} - Data: {block.data} - Hash: {block.hash}")
