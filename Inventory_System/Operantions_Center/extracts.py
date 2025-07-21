import json
from datetime import datetime

from Inventory_System.Products.product import Product
from Inventory_System.Products.state import State
from Inventory_System.Inventory_Management.stock import Stock
from Inventory_System.Inventory_Management.location import Location
from Inventory_System.People.customer import Customer
from Inventory_System.People.supplier import Supplier
from Inventory_System.Transactions.movements import Movement
from Inventory_System.Inventory_Management.inventory_record import InventoryRecord
from Inventory_System.Transactions.bills import Bill
from Inventory_System.Transactions.payment import Cash, Card

class Extracts:

    @staticmethod
    def get_movements(system):
        return [movement.to_dict() for movement in system.movements]

    @staticmethod
    def get_bills(system):
        return [bill.to_dict() for bill in system.bills.values()]

    @staticmethod
    def get_records(system):
        return [record.to_dict() for record in system.records.values()]

    @staticmethod
    def get_customers(system):
        return [customer.to_dict() for customer in system.customers.values()]

    @staticmethod
    def get_suppliers(system):
        return [supplier.to_dict() for supplier in system.suppliers.values()]

    @staticmethod
    def export_movements(system, filename="movements.json"):
        Extracts.export_to_json(Extracts.get_movements(system), filename)

    @staticmethod
    def export_records(system, filename="inventory_records.json"):
        Extracts.export_to_json(Extracts.get_records(system), filename)

    @staticmethod
    def export_customers(system, filename="customers.json"):
        Extracts.export_to_json(Extracts.get_customers(system), filename)

    @staticmethod
    def export_suppliers(system, filename="suppliers.json"):
        Extracts.export_to_json(Extracts.get_suppliers(system), filename)

    @staticmethod
    def export_bills(system, filename="bills.json"):
        Extracts.export_to_json(Extracts.get_bills(system), filename)

    @staticmethod
    def export_to_json(data, filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Exported successfully to {filename}")
        except Exception as e:
            raise ValueError(
                f"Error exporting to {filename}: {e}"
            )

    @staticmethod
    def export_full_system(system, filename="full_backup.json"):
        data = {
            "movements": Extracts.get_movements(system),
            "bills": Extracts.get_bills(system),
            "records": Extracts.get_records(system),
            "customers": Extracts.get_customers(system),
            "suppliers": Extracts.get_suppliers(system)
        }
        Extracts.export_to_json(data, filename)

    @staticmethod
    def import_all_products(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return [Extracts.dict_to_product(d) for d in data]

    @staticmethod
    def dict_to_product(data):
        name = data["name"]
        category = data["category"]
        code = data["code"]
        price = data["price"]
        state_data = data["state"]

        if isinstance(state_data, dict):
            if "expiration_date" in state_data:
                expiration = tuple(state_data["expiration_date"])
                state = State(expiration_date=expiration)
            elif "condition" in state_data:
                state = State(state_data["condition"])
            else:
                raise ValueError("Unknown format for product state")
        elif isinstance(state_data, str):
            state = State(state_data)
        else:
            raise ValueError("Unsupported type for product state")

        return Product(name, category, code, price, state)
    
    @staticmethod
    def dict_to_stock(data, system):
        actual = data["actual_stock"]
        min_stock = data["minimum_stock"]
        max_stock = data["maximum_stock"]
        
        stock = Stock(actual, min_stock, max_stock)

        if system and "record" in data:
            seen = set()
            for movement_data in data["record"]:
                code = movement_data["Code"]
                if code in system.records:
                    try:
                        movement = Extracts.dict_to_movement(
                            movement_data, system
                        )
                        key = (
                            movement.product._code, movement.amount,
                            movement.actor._id, movement.date.isoformat()
                        )
                        if key not in seen:
                            stock._record.append(movement)
                            seen.add(key)
                    except Exception as e:
                        raise ValueError(
                            f"Couldn't load movement for {code}: {e}"
                        )

        return stock
        
    @staticmethod
    def dict_to_location(data):
        aisle = data["aisle"]
        shelf = data["shelf"]

        return Location(aisle, shelf)
    
    @staticmethod
    def dict_to_customer(data):
        return Customer(data["name"], data["number_id"], data["_id"])

    @staticmethod
    def dict_to_supplier(data):
        return Supplier(data["name"], data["contact_number"], data["_id"])
    
    @staticmethod
    def dict_to_movement(data, system):
        product_code = data["Code"]
        product = system.records[product_code].product 

        amount = data["Quantity"]
        actor_id = data["Actor_ID"] 
        reason = data["Reason"]

        if data["Type"] == "in":
            actor = system.suppliers.get(actor_id)
        else:
            actor = system.customers.get(actor_id)

        if actor is None:
            raise ValueError(f"Actor with ID {actor_id} not found in system")

        return Movement(product, amount, actor, reason)
    
    @staticmethod
    def dict_to_inventory_record(data, system):
        product = Extracts.dict_to_product(data["product"])
        stock = Extracts.dict_to_stock(data["stock"], system)
        location = Extracts.dict_to_location(data["location"])

        return InventoryRecord(product, stock, location)
    
    @staticmethod
    def dict_to_bill(data, system):     
        bill_id = data["bill_id"]
        date = data["date"]
        entity_type = data["entity_type"]
        entity_id = data.get("entity_id") 
        payment_data = data["payment_method"]

        if entity_type == "Customer":
            entity = system.customers.get(entity_id)
        else:
            entity = system.suppliers.get(entity_id)

        if entity is None:
            raise ValueError(f"Entity '{entity_id}' not found in system.")

        if payment_data["method"] == "Cash":
            payment = Cash(payment_data["cash_given"])
        elif payment_data["method"] == "Card":
            card_number = str(payment_data["card_number"])[-4:]  
            payment = Card("**** **** **** " + card_number, "***")  
        else:
            raise ValueError("Unknown payment method.")

        bill = Bill(entity, payment)
        bill._bill_id = bill_id
        bill.date = datetime.strptime(date, "%Y-%m-%d")

        for item_data in data["items"]:
            product_code = item_data["product"]["_code"]
            product = system.records[product_code].product
            quantity = item_data["quantity"]
            price = item_data["price"]
            bill.add_item(product, quantity, price)

        return bill
    
    @staticmethod
    def load_inventory_records(path, system):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for record_data in data:
            record = Extracts.dict_to_inventory_record(record_data, system)
            system.add_record(record)
        Location.sync_from_inventory(system.records.values())

        print(f"{len(data)} inventory records loaded into system.")

    @staticmethod
    def load_full_backup(path, system):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for customer in data["customers"]:
            system.add_customer(Extracts.dict_to_customer(customer))
        for supplier in data["suppliers"]:
            existing = next(
                (
                    x for x in system.suppliers.values() 
                    if x.name == supplier["name"] 
                    and x.contact_number == supplier["contact_number"]
                ), None
            )
            if not existing:#*********, porque solo supplier?
                system.add_supplier(Extracts.dict_to_supplier(supplier))
        for record in data["records"]:
            product_code = record["product"]["code"]
            if product_code in system.records:
                old_stock = system.records[product_code].stock
                new_stock = Extracts.dict_to_stock(record["stock"], system)
                existing_keys = {
                    (
                        m.product._code, m.amount, m.actor._id,
                        m.date.isoformat()
                    )
                    for m in old_stock._record
                }
                for m in new_stock._record:
                    key = (
                        m.product._code, m.amount, m.actor._id, 
                        m.date.isoformat()
                    )
                    if key not in existing_keys:
                        old_stock._record.append(m)
            else:
                record = Extracts.dict_to_inventory_record(record, system)
                system.add_record(record)

        Location.sync_from_inventory(system.records.values())

        for movement_data in data["movements"]:
            movement = Extracts.dict_to_movement(movement_data, system)
            system.add_movement(movement, apply_stock=False)
            for movement1 in system.movements:
                code = movement1.product._code
                stock = system.records[code].stock
                key = (movement1.product._code, movement1.amount,
                    movement1.actor._id, movement1.date.isoformat())
                seen = {
                    (
                        movement_stock.product._code, movement_stock.amount,
                        movement_stock.actor._id, 
                        movement_stock.date.isoformat()
                    )
                    for movement_stock in stock._record
                }
                if key not in seen:
                    stock._record.append(movement)


        for bill_data in data.get("bills", []):
            bill = Extracts.dict_to_bill(bill_data, system)
            system.bills[bill._bill_id] = bill
            for m in system.movements:
                for item in bill.items:
                    if (m.product._code == item.product._code
                        and m.amount == item.quantity
                        and m.actor._id == bill.entity._id):
                        m._bill_id = bill._bill_id
                        break

        print(f"Backup loaded successfully from {path}")