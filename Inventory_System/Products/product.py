class Product:
    def __init__(self, name, category, code, price, state):
        self.name = name
        self.category = category
        self._code = code
        self._price = price
        self._state = state

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "code": self._code,
            "price": self._price,
            "state": self._state.to_dict() if self._state else None
        }