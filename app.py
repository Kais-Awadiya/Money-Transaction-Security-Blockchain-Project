from flask import Flask, render_template, request, redirect, url_for
import json
from blockchain import Blockchain  # Import the Blockchain class from blockchain.py

app = Flask(__name__)
blockchain = Blockchain()  # Create a blockchain instance

# Home route: Displays the blockchain and user balances
@app.route('/')
def index():
    users = blockchain.users  # Pass user balances to the template
    return render_template('index.html', blockchain=blockchain, users=users)

# Route to add a block with transaction data
@app.route('/add', methods=['POST'])
def add_block():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = float(request.form['amount'])

    try:
        # Add the transaction to the blockchain
        blockchain.add_block({"sender": sender, "receiver": receiver, "amount": amount})
    except ValueError as e:
        return f"Error: {e}", 400  # Return error if insufficient balance
    
    return redirect(url_for('index'))

# Route to mine a new block
@app.route('/mine')
def mine_block():
    blockchain.add_block({"sender": "Miner", "receiver": "Miner", "amount": 0})
    return redirect(url_for('index'))

# Route to validate the blockchain
@app.route('/validate')
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    validation_message = "The blockchain is valid." if is_valid else "The blockchain is not valid!"
    return render_template('index.html', blockchain=blockchain, users=blockchain.users, validation_message=validation_message)

# Route to reset the blockchain
@app.route('/reset', methods=['POST'])
def reset_chain():
    blockchain.reset_chain()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
