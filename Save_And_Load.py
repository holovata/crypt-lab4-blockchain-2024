import json
from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction


def save_blockchain(blockchain, filename='blockchain.json'):
    with open(filename, 'w') as file:
        chain_data = []
        for block in blockchain.chain:
            block_info = {
                'transactions': [
                    {
                        'sender': tx.sender,
                        'recipient': tx.recipient,
                        'amount': tx.amount,
                        'data': tx.data
                    } for tx in block.transactions
                ],
                'previous_hash': block.previous_hash,
                'nonce': block.nonce,
                'hash': block.hash
            }
            chain_data.append(block_info)
        json.dump(chain_data, file, indent=4)
    print("Blockchain saved to file.")


def load_blockchain(filename='blockchain.json'):
    with open(filename, 'r') as file:
        chain_data = json.load(file)
        blockchain = Blockchain()
        blockchain.chain = []

        for block_data in chain_data:
            transactions = [
                Transaction(tx['sender'], tx['recipient'], tx['amount'], tx.get('data', None))
                for tx in block_data['transactions']
            ]
            block = Block(transactions, block_data['previous_hash'])
            block.nonce = block_data['nonce']
            block.hash = block.calculate_hash()
            blockchain.chain.append(block)
        print("Blockchain loaded from file with {} blocks.".format(len(blockchain.chain)))

        return blockchain
