from datetime import datetime

from Inventory_System.People.customer import Customer
from Inventory_System.People.supplier import Supplier

class Movement:
    def __init__(self, product, amount, actor, reason, bill_id=None):
        self.product = product
        self.amount = amount
        self.date = datetime.now()

        if not isinstance(actor, (Customer, Supplier)):
            raise TypeError("actor must be a Customer or Supplier")
        self.actor = actor
        self._actor_id = actor._id
        self.actor_type = "customer" if isinstance(actor, Customer) else "supplier"
        self.type = "out" if isinstance(actor, Customer) else "in"
        self.reason = reason
        self._bill_id = bill_id
        self.final_price = (
            round(product._price * 1.08, 2) if self.type == "out" 
            else product._price
            )

    def get_delta(self):
        return self.amount if self.type == "in" else -self.amount
    
    @property
    def bill_id(self):
        return getattr(self, "_bill_id", None)

    def to_dict(self):
        return {
            "Product": self.product.name,
            "Code": self.product._code,
            "Quantity": self.amount,
            "Type": self.type,
            "Date": self.date.strftime("%Y-%m-%d"),
            "Actor": self.actor.name if self.actor else "N/A",
            "Actor_ID": self._actor_id,
            "Reason": self.reason
        }