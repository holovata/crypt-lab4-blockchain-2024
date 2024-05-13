import hashlib


# Функція для хешування даних за допомогою алгоритму SHA-256.
def hash_data(data):
    # Використання SHA-256 для генерації хешу.
    return hashlib.sha256(data.encode()).hexdigest()


class MerkleNode:
    # Конструктор вузла Merkle дерева.
    def __init__(self, left=None, right=None, data=None):
        self.left = left  # Лівий підвузол
        self.right = right  # Правий підвузол
        # Хеш вузла обчислюється по різному в залежності від того, чи є вузол листом чи внутрішнім вузлом.
        self.hash = self.calculate_hash(data)

    # Метод для обчислення хешу вузла.
    def calculate_hash(self, data):
        if data is not None:
            # Для листових вузлів хеш формується безпосередньо з даних.
            return hash_data(data)
        else:
            # Для внутрішніх вузлів хеш формується як хеш від конкатенації хешів лівого та правого підвузлів.
            return hash_data(self.left.hash + self.right.hash if self.left and self.right else '')


class MerkleTree:
    # Ініціалізація Merkle дерева.
    def __init__(self):
        self.leaves = []  # Список листків дерева.
        self.root = None  # Корінь дерева.

    # Додавання нового вузла (листка) до дерева.
    def add(self, data):
        new_node = MerkleNode(data=data)  # Створення нового вузла з даними.
        self.leaves.append(new_node)  # Додавання вузла до списку листків.
        self.recalculate_tree()  # Перерахунок структури дерева.

    # Перерахунок структури Merkle дерева.
    def recalculate_tree(self):
        nodes = self.leaves[:]  # Копіювання списку листків для початку перебудови дерева.
        while len(nodes) > 1:  # Поки не залишиться один вузол (корінь).
            if len(nodes) % 2 == 1:
                # Додавання копії останнього вузла, якщо кількість вузлів непарна.
                nodes.append(MerkleNode(data=nodes[-1].hash))
            new_level = []
            for i in range(0, len(nodes), 2):
                # Створення нових вузлів з пар вузлів попереднього рівня.
                new_level.append(MerkleNode(left=nodes[i], right=nodes[i + 1]))
            nodes = new_level
        self.root = nodes[0] if nodes else None  # Встановлення нового кореня дерева.

    # Отримання хешу кореня дерева.
    def root_hash(self):
        return self.root.hash if self.root else ''
