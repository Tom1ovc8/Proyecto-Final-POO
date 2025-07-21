class Inventory:
    def __init__(self):
        self.records = {}
        self.movements = []

    def add_record(self, record):
        code = record.product._code
        if code not in self.records:
            self.records[code] = record
        else:
            print("This product already exists in the inventory.")
    
    def get_record(self, code):#************
        return self.records.get(code)
    
    def remove_record(self, code):#*** consola
        if code in self.records:
            del self.records[code]
        else:
            print("No record found with this code.")

    def update_stock_limits(self, product_code:str, new_min:int, new_max:int):
        if product_code not in self.records:
            raise ValueError("Product not found in inventory records.")
        
        self.records[product_code].stock.update_stock_limits(new_min, new_max)  

    def add_movement(self, movement, apply_stock: bool = True):
        self.movements.append(movement)
        if apply_stock:
            product_code = movement.product._code
            delta = movement.get_delta()
            self.records[product_code].stock.update_stock(delta, movement)

    def get_movements_by_code(self, code):
        return [
            movement for movement in self.movements if 
                movement.product._code == code
        ]

    def get_critical_records(self):
        return [
            r for r in self.records.values()
            if r.stock.get_actual_stock() < r.stock.minimum_stock
        ]
        
    def restock_suggestions(self):
        return [
            {
                "Name": r.product.name,
            "Code": r.product._code,
            "Current Stock": r.stock.get_actual_stock(),
            "Minimum Required": r.stock.minimum_stock
            }
            for r in self.get_critical_records()
        ]