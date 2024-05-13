from datetime import datetime
from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction
from Save_And_Load import save_blockchain, load_blockchain


def main():
    print("\nInitializing the blockchain...")
    blockchain = Blockchain()
    current_time = datetime.utcnow().isoformat()

    print("\nCreating transactions...")
    transactions = [
        Transaction(sender="Alice", recipient="Bob", amount=50, data=current_time),
        Transaction(sender="Bob", recipient="Charlie", amount=30, data=current_time),
        Transaction(sender="Alice", recipient="Charlie", amount=20, data=current_time),
        Transaction(sender="Bob", recipient="Alice", amount=50, data=current_time),
        Transaction(sender="Bob", recipient="Alice", amount=100, data=current_time),
        Transaction(sender="Charlie", recipient="Alice", amount=60, data=current_time),
        Transaction(sender="Alice", recipient="Bob", amount=10, data=current_time),
        Transaction(sender="Charlie", recipient="Bob", amount=20, data=current_time)
    ]

    print("\nAdding transactions to the pending transactions list...")
    for tx in transactions:
        blockchain.add_transaction(tx)

    transactions_per_block = 3
    print("\nCreating blocks with a fixed number of transactions...")
    for i in range(0, len(blockchain.pending_transactions), transactions_per_block):
        end_index = i + transactions_per_block
        block_transactions = blockchain.pending_transactions[i:end_index]
        if block_transactions:
            new_block = Block(transactions=block_transactions)
            blockchain.add_block(new_block)

    print("\nSaving the blockchain to a file...")
    save_blockchain(blockchain, 'blockchain.json')

    print("\nLoading the blockchain from a file...")
    loaded_blockchain = load_blockchain('blockchain.json')

    block_number = 2
    print(f"\nAnalyzing loaded block {block_number}...")
    if block_number < len(loaded_blockchain.chain):
        specific_block = loaded_blockchain.chain[block_number]
        print(f"Loaded Block {block_number} with hash: {specific_block.hash}")

        print("\nCalculating and displaying balances for the specified block...")
        balances = loaded_blockchain.calculate_balances_until(block_number)
        for user, info in balances.items():
            print(f"User: {user}, Current Balance: {info['current']}, Min: {info['min']}, Max: {info['max']}")
    else:
        print("Invalid block number")


if __name__ == "__main__":
    main()
