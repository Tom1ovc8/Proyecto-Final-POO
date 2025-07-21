from datetime import datetime
import uuid

from Inventory_System.People.customer import Customer
from Inventory_System.People.supplier import Supplier

class BillItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def get_total_price(self):
        return self.quantity * self.price

    def to_dict(self):
        return {
            "product": {
                "_code": self.product._code
            },
            "quantity": self.quantity,
            "price": self.price,
            "total": self.get_total_price()
        }
    
class Bill:
    def __init__(self, entity, payment_method):
        self._bill_id = str(uuid.uuid4())
        self.date = datetime.now()
        self.entity = entity
        if not isinstance(entity, (Customer, Supplier)):
            raise TypeError("Entity must be a Customer or Supplier")
        
        self.entity_type = (
            "Customer" if isinstance(entity, Customer) else "Supplier"
        )
        self.payment_method = payment_method
        self.items = []

    def add_item(self, product, quantity, price):
        item = BillItem(product, quantity, price)
        self.items.append(item)

    def calculate_total(self):
        return sum(item.get_total_price() for item in self.items)   
    
    def to_dict(self):
        return {
            "bill_id": self._bill_id,
            "date": self.date.strftime("%Y-%m-%d"),
            "entity": self.entity.name,
            "entity_type": self.entity_type,
            "entity_id": self.entity._id,
            "payment_method": (
                self.payment_method.to_dict() if self.payment_method 
                else "N/A"
                ),
            "items": [item.to_dict() for item in self.items],
            "total": self.calculate_total()
        }