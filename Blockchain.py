from Block import Block
from collections import defaultdict
from Transaction import Transaction
from Merkle_Tree import MerkleTree


class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []  # Список блоків у ланцюжку
        self.difficulty = difficulty  # Рівень складності PoW
        self.pending_transactions = []  # Транзакції, які чекають додавання до блоку
        self.blockchain_merkle_tree = MerkleTree()
        self.create_genesis_block()

    def create_genesis_block(self):
        # Ініціалізація початкових балансів
        initial_transactions = [
            Transaction(sender="System", recipient="Alice", amount=1000, data="Initial balance"),
            Transaction(sender="System", recipient="Bob", amount=500, data="Initial balance")
        ]
        genesis_block = Block(transactions=initial_transactions, previous_hash="0")
        genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, block):
        # Додавання нового блоку до ланцюжка
        block.previous_hash = self.get_latest_block().hash
        block.proof_of_work(self.difficulty)
        self.chain.append(block)
        self.blockchain_merkle_tree.add(block.hash)

    def get_latest_block(self):
        # Отримання останнього блоку в ланцюжку
        return self.chain[-1]

    def calculate_blockchain_root_hash(self):
        # Розрахунок кореневого хешу за всіма хешами блоків
        temp_tree = MerkleTree()
        for block in self.chain:
            temp_tree.add(block.hash)
        return temp_tree.root_hash()

    def is_chain_valid(self):
        # Перевірка кореневого хешу всього блокчейна
        # Це забезпечує, що загальний стан блокчейна не був змінений
        if self.blockchain_merkle_tree.root_hash() != self.calculate_blockchain_root_hash():
            return False

        # Перевірка всіх блоків у ланцюжку на правильність послідовності і цілісності
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Перевірка хешу поточного блоку
            if current.hash != current.calculate_hash():
                # Якщо хеш блоку, який вже збережений, не відповідає новорозрахованому хешу,
                # це свідчить про зміну даних у блоці
                return False

            # Перевірка, чи хеш попереднього блоку відповідає збереженому значенню previous_hash в поточному блоку
            if current.previous_hash != previous.hash:
                # Якщо хеш попереднього блоку не співпадає з previous_hash поточного блоку,
                # то ланцюжок блоків порушений
                return False

        return True

    def update_balances(self, user_balances, sender, recipient, amount):
        # Оновлення балансів користувачів
        if sender != "System":  # Ігнорування транзакцій від "System"
            user_balances[sender]['current'] -= amount
            user_balances[sender]['min'] = min(user_balances[sender]['min'], user_balances[sender]['current'])
            user_balances[sender]['max'] = max(user_balances[sender]['max'], user_balances[sender]['current'])
        user_balances[recipient]['current'] += amount
        user_balances[recipient]['min'] = min(user_balances[recipient]['min'], user_balances[recipient]['current'])
        user_balances[recipient]['max'] = max(user_balances[recipient]['max'], user_balances[recipient]['current'])

    def calculate_balances_until(self, block_number):
        # Обчислення балансів користувачів до певного блоку
        user_balances = defaultdict(lambda: {'min': float('inf'), 'max': float('-inf'), 'current': 0})
        for i in range(min(block_number + 1, len(self.chain))):
            for tx in self.chain[i].transactions:
                self.update_balances(user_balances, tx.sender, tx.recipient, tx.amount)
        return user_balances

    def add_transaction(self, transaction):
        # Додавання транзакції до списку очікуючих транзакцій
        if self.calculate_balance(transaction.sender) >= transaction.amount:
            self.pending_transactions.append(transaction)
            print(f"Transaction from {transaction.sender} to {transaction.recipient} for {transaction.amount} added.")
        else:
            print(f"Error: Not enough balance for the transaction from {transaction.sender}.")

    def calculate_balance(self, sender):
        # Обчислення балансу користувача
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == sender:
                    balance -= tx.amount
                if tx.recipient == sender:
                    balance += tx.amount
        for tx in self.pending_transactions:
            if tx.sender == sender:
                balance -= tx.amount
            if tx.recipient == sender:
                balance += tx.amount
        return balance
