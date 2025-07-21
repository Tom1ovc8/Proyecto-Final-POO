class Payment:
    def __init__(self):
        pass

    def pay(self):
        raise NotImplementedError(
            "Subclasses must implement the pay() method."
        )

    def to_dict(self):
        raise NotImplementedError(
            "Subclasses must implement the to_dict() method."
        )

class Card(Payment):
    def __init__(self, number, cvv):
        super().__init__()
        self._number = number
        self._cvv = cvv

    def pay(self, amount):
        print(f"Paying {amount} with card ending in {self._number[-4:]}")
        return True

    def to_dict(self):
        return {
            "method": "Card",
            "card_number": f"**** **** **** {self._number[-4:]}"
        }
    
    def __str__(self):
        return f"Card - **** **** **** {self._number[-4:]}"


class Cash(Payment):
    def __init__(self, cash_given):
        super().__init__()
        self.cash_given = cash_given

    def pay(self, total):
        if self.cash_given >= total:
            change = self.cash_given - total
            print(f"Cash payment accepted. Change returned: {change}")
            return True
        else:
            print(f"Insufficient cash. Missing: {total - self.cash_given}")
            return False

    def to_dict(self):
        return {
            "method": "Cash",
            "cash_given": self.cash_given
        }
    
    def __str__(self):
        return f"Cash - Given: ${self.cash_given:.2f}"