class Transaction:
    def __init__(self, sender, recipient, amount, data=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.data = data  # Додаткове поле для зберігання інформації або повідомлень

    def __repr__(self):
        return f"Transaction(sender={self.sender}, recipient={self.recipient}, amount={self.amount}, data={self.data})"