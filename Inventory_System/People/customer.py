import uuid

class Customer:
    def __init__(self, name, number_id, customer_id=None):
        self.name = name
        self.number_id = number_id
        self._id = customer_id if customer_id else str(uuid.uuid4())

    def to_dict(self):
        return {
            "name": self.name,
            "number_id": self.number_id,
            "_id": self._id #*****, puede ser sin el guion???
        }