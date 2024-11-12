from flask import Flask, render_template, request, redirect, url_for
import json
from blockchain import Blockchain  # Import the Blockchain class from blockchain.py

app = Flask(__name__)
blockchain = Blockchain()  # Create a blockchain instance

# Home route: Displays the blockchain
@app.route('/')
def index():
    return render_template('index.html', blockchain=blockchain)

# Route to add a block with transaction data
@app.route('/add', methods=['POST'])
def add_block():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    # Add the transaction to the blockchain
    blockchain.add_block({"sender": sender, "receiver": receiver, "amount": float(amount)})
    
    return redirect(url_for('index'))

# Route to mine a new block
@app.route('/mine')
def mine_block():
    blockchain.add_block({"sender": "Miner", "receiver": "Miner", "amount": 0})
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
