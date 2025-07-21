from Inventory_System.Transactions.movements import Movement

class Stock:
    def __init__(self, actual_stock, minimum_stock, maximum_stock):
        self._actual_stock = actual_stock
        self.minimum_stock = minimum_stock
        self.maximum_stock = maximum_stock
        self._record = []

    def get_actual_stock(self):
        return self._actual_stock
        
    def is_valid_update(self, delta):
        new_stock = self._actual_stock + delta
        return 0 <= new_stock <= self.maximum_stock

    def update_stock(self, delta, movement):#*** Mirar si siempre manda un movement
        if not self.is_valid_update(delta):
            print("Cannot update stock.")
            return False
        if not isinstance(movement, Movement):
            raise TypeError(
                "Only Movement instances are allowed to update stock."
                )
        
        self._actual_stock += delta
        self._record.append(movement)
        return True

    def update_stock_limits(self, new_min, new_max):#**************
        if new_min < 0 or new_max < 0:
            raise ValueError("Stock limits cannot be negative.")
        if new_min > new_max:
            raise ValueError("Minimum stock cannot exceed maximum stock.")
        self.minimum_stock = new_min
        self.maximum_stock = new_max

    def show_history(self): #****** si se usa??
        for stock_record in self._record:
            print(stock_record.to_dict())           

    def to_dict(self):
        return {
            "actual_stock": self._actual_stock,
            "minimum_stock": self.minimum_stock,
            "maximum_stock": self.maximum_stock,
            "record": [mov.to_dict() for mov in self._record]
        }
    
