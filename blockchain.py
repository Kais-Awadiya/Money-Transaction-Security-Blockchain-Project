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
        self.users = {
            "Jenish": 500.00,
            "Kais": 300.00,
            "Ghata": 200.00,
            "Miner": 0.00
        }  # Dictionary to store user accounts and balances
        self.create_genesis_block()

    def create_genesis_block(self):
        # Manually create the first block in the chain (index 0)
        genesis_block = Block(0, time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        # Update user balances before adding the block
        sender = data["sender"]
        receiver = data["receiver"]
        amount = data["amount"]

        # Ensure sender and receiver are in the users dictionary
        if sender not in self.users:
            self.users[sender] = 0
        if receiver not in self.users:
            self.users[receiver] = 0

        # Deduct balance from sender and add to receiver
        if sender != "Miner":
            if self.users[sender] < amount:
                raise ValueError(f"{sender} does not have enough balance!")
            self.users[sender] -= amount
        self.users[receiver] += amount

        # Create and add the new block
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time(), data, previous_block.hash)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} has been tampered with!")
                return False

            # Check if the previous_hash of the current block matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index}'s previous hash does not match!")
                return False

            # Check if the hash meets the difficulty requirement
            if not current_block.hash.startswith('0' * current_block.difficulty):
                print(f"Block {current_block.index} does not meet difficulty requirements!")
                return False

        print("Blockchain is valid.")
        return True
    
    def reset_chain(self):
        # Clear the chain and create a new genesis block
        self.chain = []
        self.create_genesis_block()