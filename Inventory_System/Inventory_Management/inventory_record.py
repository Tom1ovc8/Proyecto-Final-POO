class InventoryRecord:
    def __init__(self, product, stock, location):
        self.product = product
        self.stock = stock
        self.location = location

    def to_dict(self):
        return {
            "product": self.product.to_dict(),
            "stock": self.stock.to_dict(),
            "location": self.location.to_dict()
        }