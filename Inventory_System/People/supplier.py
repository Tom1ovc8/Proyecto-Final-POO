import uuid

class Supplier:
    def __init__(self, name, contact_number, supplier_id=None):
        self.name = name
        self.contact_number = contact_number
        self._id = supplier_id if supplier_id else str(uuid.uuid4())

    def to_dict(self):
        return {
            "name": self.name,
            "contact_number": self.contact_number,
            "_id": self._id
        }