from Merkle_Tree import MerkleTree, hash_data


class Block:
    def __init__(self, transactions, previous_hash=''):
        # Список транзакцій в блоці.
        self.transactions = transactions
        # Хеш попереднього блоку в ланцюгу.
        self.previous_hash = previous_hash
        # Змінна для виконання proof-of-work.
        self.nonce = 0
        # Ініціалізація Merkle дерева для транзакцій у блоку.
        self.merkle_tree = MerkleTree()
        for transaction in transactions:
            # Додавання репрезентації кожної транзакції до Merkle дерева.
            self.merkle_tree.add(transaction.__repr__())
        # Розрахунок початкового хешу блоку.
        self.hash = self.calculate_hash()

    # Метод для розрахунку хешу блоку.
    def calculate_hash(self):
        # Створення рядка, який включає хеш попереднього блоку, nonce і хеш кореня Merkle дерева.
        block_string = f"{self.previous_hash}{self.nonce}{self.merkle_tree.root_hash()}"
        # Генерація хешу з цього рядка.
        return hash_data(block_string)

    # Реалізувати “proof-of-work” для додавання блоку.
    def proof_of_work(self, difficulty):
        # Кількість початкових нулів у хеші.
        target = '0' * difficulty
        # Поки генерований хеш не відповідає цілі, збільшувати nonce і перераховувати хеш.
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        # Вивід хешу блоку.
        print(f"Block with PoW: {self.hash}")
