<h1 align="center"> Inventory Management - Stokapp </h1>

<h2 align="center"> Final OOP Project </h2>

The main goal of this project is build an application that simulates an inventory management system for a warehouse using a graphical user interface (GUI). 
The program includes operations such as:
  - Creating objects to be stored  
  - Registering incoming and outgoing inventory
  - Retrieving a list of current inventory
  - Handling dates in inventory records

In addition, it offers extra features like:
  + Bulk record upload
  + File handling for data persistence
  + Report generation in document format

<h2 align="center"> Index </h2>

- [Class Diagram]()
- [Products]()
  - [Product]()
  - [State]()
- [Inventory_Management]()
  - [Inventory_Record]()
  - [Location]()
  - [Stock]()
  - [Inventory]()
- [People]()
  - [Customer]()
  - [Supplier]()
- [Transactions]()
  - [Movements]()
  - [Payment]()
  - [Bills]()
- [Operations_Center]()
  - [System]()
  - [Extracts]()
  - [Generatepdf]()
  - [App]()

-----------

<h3 align="center"> Class Diagram </h3>

-----------

<h3 align="center"> Products </h3>


#### Product


In the `Product` class, through the `__init__` method, we define the products that will be part of our inventory system. Each product has five main attributes: `name`, `category`, `code`, `price`, and `state`. The `name` attribute represents the product’s commercial name, while `category` allows us to classify it within a general category (such as "Vegetables" or "Grains"). The `code` field, which is protected using an underscore (`_code`), corresponds to the internal identifier of the product, allowing it to be distinguished from others in the system. Similarly, `price` (also protected as `_price`) indicates the monetary value of the product, and `state` is an object that describes its current status. The latter can be `None` if no state is defined at the time the product is created.


```python
class Product:
    def __init__(self, name, category, code, price, state):
        self.name = name
        self.category = category
        self._code = code
        self._price = price
        self._state = state
```

With the `to_dict` method, we convert each instance of `Product` into a Python dictionary, which is useful for tasks like storing data in databases using JSON. The dictionary includes keys such as `"name"`, `"category"`, `"code"`, `"price"`, and `"state"`, and their respective values correspond to the object's attributes. In particular, if the `_state` attribute exists, it will also be converted into a dictionary using its own `to_dict` method; otherwise, it will be recorded as `None`.

```python
    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "code": self._code,
            "price": self._price,
            "state": self._state.to_dict() if self._state else None
        }
```
This structure allows us to keep all the product information organized and easily accessible for processing within the inventory system.



#### State

The `State` class represents the condition in which a product in the inventory is found. Each instance must contain at least one of the two attributes: a `condition` or an `expiration_date`. Although both parameters are optional in the constructor’s signature, the system’s logic assumes that at least one of them must be present for the state to be meaningful.


```python
class State:
    def __init__(self, condition = None, expiration_date = None):
        self._condition = condition
        self._expiration_date = expiration_date
```

The `_condition` attribute is a string that can represent, for example, that the product is "Fresh" (this is used for products like `Fruits` or `Vegetables`). On the other hand, `_expiration_date` must be provided as a tuple of three values (`YYYY`, `MM`, `DD`), and it represents the date on which the product is no longer valid or useful (this is used for packaged products with a specific expiration date). Although neither field is required individually, the system expects at least one of them to be defined.

One of the core methods is `is_expired`, which allows checking whether the product’s expiration date has already passed. If `_expiration_date` is defined, it is converted into a `datetime.date` object and compared with the current date. If the product has no expiration date, the method simply returns `False`.


```python
    def is_expired(self):
        if self._expiration_date:
            today = datetime.date.today()
            expiration = datetime.date(*self._expiration_date)
            return today > expiration
        return False
```
The `to_dict` method converts the product's state into a dictionary. If the state has a condition, it will be included under the `"condition"` key; if it has an expiration date, it will be included as `"expiration_date"`. If both are present, both will be reflected in the dictionary.

```python
    def to_dict(self):
        state_dict = {}
        if self._condition is not None:
            state_dict["condition"] = self._condition
        if self._expiration_date is not None:
            state_dict["expiration_date"] = self._expiration_date
        return state_dict
```
Additionally, the class implements the special method `__str__`, which generates a readable representation of the product's state. If a valid condition exists, it will be shown as `"Condition: <condition>"`. If there is an expiration date, it will be displayed in the format `"Expires: YYYY-MM-DD"`. When both attributes exist, they are concatenated separated by a comma; if neither is present (although this should not happen according to the system logic), the string `"Unknown"` is returned.

```python
    def __str__(self):
        state_parts = []
        if isinstance(self._condition, str):
            state_parts.append(f"Condition: {self._condition}")
        if self._expiration_date:
            date = datetime.date(*self._expiration_date)
            date_str = date.strftime("%Y-%m-%d")
            state_parts.append(f"Expires: {date_str}")
        return ", ".join(state_parts) if state_parts else "Unknown"
```
In summary, the `State` class allows describing the physical or temporal condition of a product, ensuring that there is at least one criterion to determine whether the product is usable, expired, or needs inspection. This class can be easily integrated with other parts of the system through its `to_dict` and `__str__` methods.

-----------

<h3 align="center"> Inventory_Management </h3>

#### Inventory Record:

In the `InventoryRecord` class, the `__init__` method defines the attributes that the inventory record will have, such as `product`, `stock`, and `location`. These will act as objects.

```python
class InventoryRecord:
    def __init__(self, product, stock, location):
        self.product = product
        self.stock = stock
        self.location = location
```

We reference the attributes of our `InventoryRecord` class through our constructor `self` using the names `product`, `stock`, and `location`.

```python
    def to_dict(self):
        return {
            "product": self.product.to_dict(),
            "stock": self.stock.to_dict(),
            "location": self.location.to_dict()
        }
```

We convert the attributes of our `InventoryRecord` class into a dictionary with the keys: `product`, `stock`, and `location`.

#### Location:

We create the `Location` class to which we assign some protected attributes outside the constructor that are shared among all instances of the class. These are `_category_aisles`, which is the category of each aisle and is an empty dictionary; `_next_aisle_number`, which dictates the next aisle number, incrementing one by one; `_shelf_counter_by_category`, which counts how many shelves have been assigned per category (also an empty dictionary); and `_product_shelving = {}`, which is a dictionary of each product’s shelving.

```python
class Location:
    _category_aisles = {}
    _next_aisle_number = 1
    _shelf_counter_by_category = {}
    _product_shelving = {}
```

We define the attributes of our `Location` class, which are `aisle` (aisles) and `shelf` (shelves).


```python
    def __init__(self, aisle, shelf):
        self.aisle = aisle
        self.shelf = shelf
```

With the `@classmethod` decorator, we indicate that the method works with the entire class. We define the `sync_from_inventory` method so that, for each record in the records dictionary, an aisle and shelf are assigned, and the variables `category`, `code`, `aisle`, and `shelf` are taken.

```python
    @classmethod
    def sync_from_inventory(cls, records):
        for record in records:
            category = record.product.category
            code = record.product._code
            aisle = int(record.location.aisle)
            shelf = int(record.location.shelf)
```

If the category is not assigned to a specific aisle, this method will assign it an available one.

```python
    @classmethod
    def sync_from_inventory(cls, records):
        for record in records:
            category = record.product.category
            code = record.product._code
            aisle = int(record.location.aisle)
            shelf = int(record.location.shelf)

            if category not in cls._category_aisles:
                cls._category_aisles[category] = aisle
                cls._next_aisle_number = max(cls._next_aisle_number, aisle+1)
            cls._product_shelving[(category, code)] = shelf
            cls._shelf_counter_by_category[category] = max(
                cls._shelf_counter_by_category.get(category, 0),
                shelf
            )
```

With the `@classmethod` decorator, we indicate that the method works with the entire class and not just individual objects. We define the `assign_location` method. If the `category` instance does not have an assigned aisle, it will be assigned an available one, so that if one aisle is occupied, the next one will be checked until an available one is found. The variables `aisle` and `key` will be used.

```python
    @classmethod
    def assign_location(cls, category, code):
        if category not in cls._category_aisles:
            cls._category_aisles[category] = cls._next_aisle_number
            cls._next_aisle_number += 1
        aisle = cls._category_aisles[category]
        key = (category, code)
```

If the `key` is in an aisle, the variable `shelf` will be assigned to it. If not, an available aisle will be assigned, starting from 0 and checking one by one to see which is available.

```python
        if key in cls._product_shelving:
            shelf = cls._product_shelving[key]
        else:
            cls._shelf_counter_by_category.setdefault(category, 0)
            cls._shelf_counter_by_category[category] += 1
            shelf = cls._shelf_counter_by_category[category]
            cls._product_shelving[key] = shelf
        return cls(aisle, shelf)
```

Through the `to_dict` method, we convert the product location information into a dictionary with the keys `aisle` and `shelf`.


```python
    def to_dict(self):
        return {
            "aisle": self.aisle,
            "shelf": self.shelf
        }
```

#### Stock:

From the `Inventory_System.Transactions.movements` module, we import the `Movement` class.

```python
from Inventory_System.Transactions.movements import Movement
```

We create the `Stock` class with attributes such as `actual_stock`, `minimum_stock`, `maximum_stock`, and `_record`, which is an empty list.

```python
    def __init__(self, actual_stock, minimum_stock, maximum_stock):
        self._actual_stock = actual_stock
        self.minimum_stock = minimum_stock
        self.maximum_stock = maximum_stock
        self._record = []
```

The `get_actual_stock` method is defined, which, when called to check the current stock, will return it to us.

```python
    def get_actual_stock(self):
        return self._actual_stock
```

The `is_valid_update` method is defined with an attribute `delta` that represents the stock change. The method checks that before modifying the stock, the change does not leave the stock below the minimum or above the maximum allowed.

```python
    def is_valid_update(self, delta):
        new_stock = self._actual_stock + delta
        return 0 <= new_stock <= self.maximum_stock
```

The `update_stock` method is defined to update the stock of a product. Through this method, if the stock update is not valid, it will return the message `"Cannot update stock"`. If it is valid, the `delta` movement will be added to the current stock, whether it is incoming or outgoing. If a movement is passed, it is saved in the records dictionary; otherwise, it returns the message `"Only Movement instances are allowed to update stock"`.

```python
    def update_stock(self, delta, movement):
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
```

We define the `update_stock_limits` method with the instances `new_min` and `new_max` to update the minimum and maximum stock of a product. If there is an attempt to update the minimum or maximum stock to a value less than 0, it will return the error message `"Stock limits cannot be negative"`. If the minimum stock is updated to be higher than the maximum stock, it will return the error message `"Minimum stock cannot exceed maximum stock"`. If the change is valid, it will be updated.

```python
    def update_stock_limits(self, new_min, new_max):
        if new_min < 0 or new_max < 0:
            raise ValueError("Stock limits cannot be negative.")
        if new_min > new_max:
            raise ValueError("Minimum stock cannot exceed maximum stock.")
        self.minimum_stock = new_min
        self.maximum_stock = new_max
```

The `to_dict` method returns the current stock, minimum stock, and maximum stock in a dictionary with the keys `actual_stock`, `minimum_stock`, and `maximum_stock`.

```python
    def to_dict(self):
        return {
            "actual_stock": self._actual_stock,
            "minimum_stock": self.minimum_stock,
            "maximum_stock": self.maximum_stock,
            "record": [mov.to_dict() for mov in self._record]
        }    
```

#### Inventory:

In the `Inventory` class, we define two attributes where we will store data, which are created directly from the object without needing to receive them as parameters. These are: `self.records`, which is an empty dictionary, and `self.movements`, which is an empty list.

```python
class Inventory:
    def __init__(self):
        self.records = {}
        self.movements = []
```

We define the function `add_record`, which will help us add a record to the records dictionary using the product code, in case it is not already in the dictionary. If the product is already in the dictionary, it returns an error message: `"This product already exists in the inventory"`.

```python
    def add_record(self, record):
        code = record.product._code
        if code not in self.records:
            self.records[code] = record
        else:
            print("This product already exists in the inventory.")
```

The function `remove_record` was defined to, as its name suggests, remove a product’s record by code using the `del` statement. The function will look for the code in the records library. If the code is found, the function proceeds correctly and deletes the record from the library. If the code is not found, the system throws the message "*No record found with this code*".

```python
    def remove_record(self, code):
        if code in self.records:
            del self.records[code]
        else:
            print("No record found with this code.")
```

The `update_stock_limits` method is defined, which will update the allowed minimum and maximum stock limits for a product. If the product code is not found in the records dictionary, it will return the error message `"Product not found in inventory records"`.

```python
    def update_stock_limits(self, product_code:str, new_min:int, new_max:int):
        if product_code not in self.records:
            raise ValueError("Product not found in inventory records.") 
        self.records[product_code].stock.update_stock_limits(new_min, new_max)
```

Each quantity change (defined as `movement`), whether incoming or outgoing, will be stored in the movements list with the command `self.movements.append(movement)`. If the stock update applies, it will then be saved in the records dictionary by product code (`product_code`). `delta` is defined as the inventory quantity change, either positive or negative. Afterwards, the stock is updated with the command `self.records[product_code].stock.update_stock(delta, movement)`, which takes the product code, and the `update_stock()` method of `stock` is responsible for updating the product’s inventory.

```python
    def add_movement(self, movement, apply_stock: bool = True):
        self.movements.append(movement)
        if apply_stock:
            product_code = movement.product._code
            delta = movement.get_delta()
            self.records[product_code].stock.update_stock(delta, movement)
```

In case you want to check each movement, the function `get_movements_by_code` was defined, which allows querying all movements in the form of a list for a specific product by its code.

```python
    def get_movements_by_code(self, code):
        return [
            movement for movement in self.movements if 
                movement.product.code == code
        ]
```

The `get_critical_records` method is used to return all product records whose current stock is below the minimum allowed, for each record in the records dictionary.

```python
    def get_critical_records(self):
        return [
            r for r in self.records.values()
            if r.stock.get_actual_stock() < r.stock.minimum_stock
        ]
```

The `restock_suggestions` method suggests which products need to be restocked according to the established minimum, meaning those with stock below it. It takes the products from the list returned by the `get_critical_records` method and returns their values with the keys `Name`, `Code`, `Current Stock`, and `Minimum Required`.

```python
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
```
-----------

<h3 align="center"> People </h3>

#### Customer:

In the `Customer` class, through the `__init__` method, we define our customer with main attributes such as `name`, `number_id`, and `customer_id`.

```python
import uuid

class Customer:
    def __init__(self, name, number_id, customer_id=None):
        self.name = name
        self.number_id = number_id
        self._id = customer_id if customer_id else str(uuid.uuid4())
```

Using the constructor `self`, we reference the attributes that our `Customer` class will have: `name`, `number_id`, and a `customer_id` for which we use the `uuid` library to generate a universally unique identifier (UUID) for each customer, ensuring these identifiers do not repeat for security reasons, as it is extremely unlikely. With UUID version `uuid4`, we obtain a completely random identifier, which exponentially increases security; however, if needed, the customer's identifier can also be manually assigned.

```python
    def to_dict(self):
        return {
            "name": self.name,
            "number_id": self.number_id,
            "_id": self._id
        }
```
 
With the `to_dict` method, we convert the objects of the `Customer` class into a Python dictionary with the keys: `name`, `number_id`, and `_id`.

#### Supplier:

In the `Supplier` class, through the `__init__` method, we also define our supplier with main attributes such as `name`, `contact_number`, and `supplier_id`.

```python
import uuid

class Supplier:
    def __init__(self, name, contact_number, supplier_id=None):
        self.name = name
        self.contact_number = contact_number
        self._id = supplier_id if supplier_id else str(uuid.uuid4())
```

Using the constructor `self`, we also reference the attributes of our `Supplier` class, which are similar but not the same as those of the previous class. In this case, the attributes are `name`, `contact_number` (which differs from the `Customer` class), and `supplier_id`, which, like in the previous class, we randomize using UUID version `uuid4`.

```python
    def to_dict(self):
        return {
            "name": self.name,
            "contact_number": self.contact_number,
            "_id": self._id
        }
```

As with the previous class, we convert the objects of our `Supplier` class into a dictionary with the keys: `name`, `contact_number`, and `_id`.

-----------

<h3 align="center"> Transactions </h3>

#### Movements:

We import the `datetime` library, and from the `Inventory_System.People` module, we import `Customer` and `Supplier`.

```python
from datetime import datetime
from Inventory_System.People.customer import Customer
from Inventory_System.People.supplier import Supplier
```

The `Movement` class represents an individual inventory movement record. Each movement is related to a product, an amount (`amount`), a reason or motive for the movement, and an actor (customer or supplier) that generates it. The date is also recorded, and it is determined whether the movement is incoming or outgoing.

The `__init__` constructor is a method that initializes a new movement with the provided information: the involved product, the quantity of units, the actor (customer or supplier) performing it, and the reason for the movement.

```python
class Movement:
    def __init__(self, product, amount, actor, reason):
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
```
- The reference to the product and the quantity (`amount`) are stored directly.

- `datetime.now()` is used to capture the date of the movement at the moment of its creation.

- It validates that the actor is an instance of either `Customer` or `Supplier`; otherwise, it raises a `TypeError`.

- The actor's identifier (`_actor_id`) is stored, and the actor is classified as either a customer or a supplier using `actor_type`.

- Automatically, the type of movement is set to `"out"` if performed by a customer (inventory outgoing), or `"in"` if performed by a supplier (inventory incoming).

- Finally, the reason for the movement is saved.

The `get_delta` method calculates the change this movement represents on the product's inventory.

```python
    def get_delta(self):
        return self.amount if self.type == "in" else -self.amount
```
- If the movement is incoming (`"in"`), it returns the quantity as a positive value.

- If the movement is outgoing (`"out"`), it returns the quantity as a negative value.

- This result can be used directly to update the product's inventory.

The `to_dict` method converts the movement into a Python dictionary, ideal for serialization, storage, or structured printing.

```python
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
```
It returns key information about the movement, such as the product’s name and code, the quantity, the movement type (`in` or `out`), the formatted date, the actor’s name and ID, and the recorded reason.

#### Payment:
In the `Payment` class, we define an abstract base class for all payment methods. That is, this class will not be used directly to make payments, but serves as a template for child classes like `Card` and `Cash`. In it, we define two methods (`pay` and `to_dict`) that must be implemented by the subclasses.

```python
class Payment:
    def __init__(self):
        pass

    def pay(self, amount):
        raise NotImplementedError("Subclasses must implement the pay() method.")

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement the to_dict() method.")
```

The `Card` class inherits from `Payment` and represents a card payment method. In its constructor (`__init__`), we receive the card number and the CVV code. We use `super()` to call the base class constructor.

```python
class Card(Payment):
    def __init__(self, number, cvv):
        super().__init__()
        self._number = number
        self._cvv = cvv
```
The `pay` method in this class simulates the action of paying by card. It prints a console message indicating how much will be paid and shows the last 4 digits of the card number.

```python
    def pay(self, amount):
        print(f"Paying {amount} with card ending in {self._number[-4:]}")
        return True
```

The `to_dict` method converts the card data into a dictionary, hiding the full number for security reasons. It only shows the last 4 digits.

```python
    def to_dict(self):
        return {
            "method": "Card",
            "card_number": f"**** **** **** {self._number[-4:]}"
        }
```

Finally, with the `__str__` method, we return a readable text representation of the `Card` object, also showing only the last digits of the number.

```python
    def __str__(self):
        return f"Card - **** **** **** {self._number[-4:]}"
```

The `Cash` class also inherits from `Payment`, but represents cash payments. In its constructor, it stores the amount given by the customer.

```python
class Cash(Payment):
    def __init__(self, cash_given):
        super().__init__()
        self.cash_given = cash_given
```

The `pay` method checks if the cash provided is enough to cover the payment amount. If sufficient, it calculates the change and prints it; if not, it informs how much is missing.

```python
    def pay(self, amount):
        if self.cash_given >= amount:
            change = self.cash_given - amount
            print(f"Cash payment accepted. Change returned: {change}")
            return True
        else:
            print(f"Insufficient cash. Missing: {amount - self.cash_given}")
            return False
```

The `to_dict` method converts the cash payment data into a dictionary that stores the method and the amount given.

```python
    def to_dict(self):
        return {
            "method": "Cash",
            "cash_given": self.cash_given
        }
```

Finally, `__str__` returns a readable representation of the `Cash` object, indicating how much money the customer provided.

```python
    def __str__(self):
        return f"Cash - Given: ${self.cash_given:.2f}"
```

#### Bills:
This module allows managing purchase or sales invoices associated with an entity (either a customer or a supplier), including a list of products, their quantities, prices, and the corresponding payment method.

The `BillItem` class represents a single item within an invoice. It contains three essential attributes: the `product`, the `quantity` purchased, and the unit `price` of that product.

```python
class BillItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
```

With the `get_total_price` method, we calculate the total price of the item by multiplying the quantity by the unit price.

```python
    def get_total_price(self):
        return self.quantity * self.price
```

The `to_dict` method allows converting the item into a Python dictionary, useful for serialization or storage. It includes the product’s name and code, the quantity, unit price, and total.

```python
    def to_dict(self):
        return {
            "Product": self.product.name,
            "Code": self.product._code,
            "Quantity": self.quantity,
            "Price": self.price,
            "Total": self.get_total_price()
        }
```

The `Bill` class represents a complete invoice. It includes an entity (which can be a customer or a supplier), the issue date, a unique identifier, the payment method, and a list of items (`BillItem`) that compose the invoice.

```python
class Bill:
    def __init__(self, entity, payment_method):
        self._bill_id = str(uuid.uuid4())
        self.date = datetime.now()
        self.entity = entity
        self.entity_type = "Customer" if isinstance(entity, Customer) else "Supplier"
        self.payment_method = payment_method
        self.items = []
```
In this constructor, a unique ID for the invoice is automatically generated using `uuid4`, and the current date is recorded using `datetime.now()`. The entity type (`Customer` or `Supplier`) is identified by checking the class of the received object. The empty list of items that will later be added to the invoice is also initialized.

With the `add_item` method, products are added to the invoice. A new `BillItem` object is created with the product, quantity, and price, and then added to the list of items.

```python
    def add_item(self, product, quantity, price):
        item = BillItem(product, quantity, price)
        self.items.append(item)
```

The `calculate_total` method sums the total of all items that have been added to the invoice, using the `get_total_price` function defined in each `BillItem`.

```python
    def calculate_total(self):
        return sum(item.get_total_price() for item in self.items)
```

Finally, `to_dict` converts all the invoice information into a structured dictionary. This includes the ID, the date in year-month-day format, the entity’s name, its type, the payment method (converted to a dictionary if present), the list of items (also as dictionaries), and the grand total.

```python
    def to_dict(self):
        return {
            "bill_id": self._bill_id,
            "date": self.date.strftime("%Y-%m-%d"),
            "entity": self.entity.name,
            "entity_type": self.entity_type,
            "payment_method": self.payment_method.to_dict() if self.payment_method else "N/A",
            "items": [item.to_dict() for item in self.items],
            "total": self.calculate_total()
        }
```

-----------

<h3 align="center"> Operations_Center </h3>

<h3 align="left"> Extracts </h3>

The `Extracts` class encapsulates all operations related to exporting, importing, and reconstructing data from the inventory system.


*It is important to clarify that, at the beginning of each method, the `@staticmethod` decorator is used in all methods of the `Extracts` class because these methods do not need to access or modify any attribute or internal state of a specific instance of the class. That is, their behavior depends exclusively on the data they receive as arguments, not on internal properties of `self`. Using `@staticmethod` in this context allows organizing export and import utilities functionally within the same class, without needing to create instances of it, which is more efficient and clearer from a software design point of view.*

<h4 align="left"> Queries: retrieving data from the system as lists of dictionaries: </h4>

```python
@staticmethod
def get_movements(system):
    return [movement.to_dict() for movement in system.movements]
```

This method iterates over all movements (`system.movements`) and calls `to_dict()` on each one, converting them into dictionaries to facilitate their export.

```python
@staticmethod
def get_bills(system):
    return [bill.to_dict() for bill in system.bills.values()]
```
This method extracts all invoices from the system (`system.bills` is a dictionary), converts them to dictionaries using `to_dict()`, and returns a list with all of them.

```python
@staticmethod
def get_records(system):
    return [record.to_dict() for record in system.records.values()]
```
This method converts all inventory records (which contain products and stock) into dictionary format.

```python
@staticmethod
def get_customers(system):
    return [customer.to_dict() for customer in system.customers.values()]
```
This method returns all customers in the system as a list of dictionaries, useful for saving or reconstructing them later.

```python
@staticmethod
def get_suppliers(system):
    return [supplier.to_dict() for supplier in system.suppliers.values()]
```
This method is similar to the previous one, but for suppliers.

#### Generic data export to `.json` files
```python
@staticmethod
def export_to_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Exported successfully to {filename}")
    except Exception as e:
        raise ValueError(f"Error exporting to {filename}: {e}")
```
This method saves any `data` (a list of dictionaries) into a `.json` file.

- It uses indentation to make the file readable.

- `ensure_ascii=False` allows saving special characters (like accents).

- It catches write errors and raises an explanatory exception.

<h4 align="left"> Specific exports by object type </h4>

Each of these methods uses the previous (`get_...`) methods and the general exporter:

```python
@staticmethod
def export_movements(system, filename="movements.json"):
    Extracts.export_to_json(Extracts.get_movements(system), filename)
```
This method exports all system movements to `movements.json`.

```python
@staticmethod
def export_bills(system, filename="bills.json"):
    Extracts.export_to_json(Extracts.get_bills(system), filename)
```
This method exports all invoices to `bills.json`.

<h4 align="left"> Full system export </h4>

```python
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
```

This method creates a dictionary with all the system’s key data and exports it into a single file. This file can be used as a general backup or to load the entire system at another time.

<h4 align="left"> Importing products from a JSON file </h4>

```python
@staticmethod
def import_all_products(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return [Extracts.dict_to_product(d) for d in data]
```
This method opens the `filename`, then loads the data as a list of dictionaries (`data`), and for each dictionary calls the `dict_to_product` method to convert it into a `Product` object.

<h4 align="left"> Product reconstruction </h4>

```python
@staticmethod
def dict_to_product(data):
    name = data["name"]
    category = data["category"]
    code = data["code"]
    price = data["price"]
    state_data = data["state"]
```

This block extracts the essential fields from the `data` dictionary to then determine the type of state:

```python
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
```
What this method does is that if the state is a dictionary with `"expiration_date"`, it converts it into a tuple and creates a `State`. If it has `"condition"`, it creates a `State` with that condition, and if the data type is not compatible, it raises `ValueError` exceptions, to finally:

```python
return Product(name, category, code, price, state)
```
Return a complete `Product` object ready to be used.

<h4 align="left"> Converting entities from dictionaries </h4>

```python
@staticmethod
def dict_to_customer(data):
    return Customer(data["name"], data["number_id"], data["_id"])
```
This method reconstructs the `Customer` object from a dictionary to be used when loading backups.
```python
@staticmethod
def dict_to_supplier(data):
    return Supplier(data["name"], data["contact_number"], data["_id"])
```
This method does the same, but this time with the `Supplier` object.

<h4 align="left"> Stock reconstruction (quantity, minimums, history) </h4>

```python
@staticmethod
def dict_to_stock(data, system):
    actual = data["actual_stock"]
    min_stock = data["minimum_stock"]
    max_stock = data["maximum_stock"]
    stock = Stock(actual, min_stock, max_stock)
```
This method creates the `Stock` object with its minimum and maximum parameters, then reconstructs the history.

```python
if system and "record" in data:
    seen = set()
    for movement_data in data["record"]:
        code = movement_data["Code"]
        if code in system.records:
            movement = Extracts.dict_to_movement(movement_data, system)
            key = (movement.product._code, movement.amount, movement.actor._id, movement.date.isoformat())
            if key not in seen:
                stock._record.append(movement)
                seen.add(key)
```
What this method does is, if there is a movement history (`record`), it reconstructs it, avoiding duplicate movements by using a set (`seen`) of unique keys.

<h4 align="left"> Movement conversion </h4>

```python
@staticmethod
def dict_to_movement(data, system):
    product_code = data["Code"]
    product = system.records[product_code].product
    amount = data["Quantity"]
    actor_id = data["Actor_ID"]
    reason = data["Reason"]
```

This method retrieves the fields in the movement. Then:

```python
if data["Type"] == "in":
    actor = system.suppliers.get(actor_id)
else:
    actor = system.customers.get(actor_id)

if actor is None:
    raise ValueError(f"Actor with ID {actor_id} not found in system")

return Movement(product, amount, actor, reason)
```
This method determines if the actor is a supplier or customer based on the movement type. It creates a `Movement` with the corresponding data.

<h4 align="left"> Invoice reconstruction </h4>

```python
@staticmethod
def dict_to_bill(data, system):
    bill_id = data["bill_id"]
    date = data["date"]
    entity_type = data["entity_type"]
    entity_id = data.get("entity_id")
    payment_data = data["payment_method"]
```
This method extracts the basic invoice data. Then:

```python
if entity_type == "Customer":
    entity = system.customers.get(entity_id)
else:
    entity = system.suppliers.get(entity_id)

# reconstruir método de pago
if payment_data["method"] == "Cash":
    payment = Cash(payment_data["cash_given"])
elif payment_data["method"] == "Card":
    card_number = str(payment_data["card_number"])[-4:]
    payment = Card("**** **** **** " + card_number, "***")
else:
    raise ValueError("Unknown payment method.")
```
This method creates the entity object and the appropriate payment method. Then the invoice is created and its ID and date are set:

```python
bill = Bill(entity, payment)
bill._bill_id = bill_id
bill.date = datetime.strptime(date, "%Y-%m-%d")
```
Finally, the invoiced products are added:

```python
for item_data in data["items"]:
    product_code = item_data["product"]["_code"]
    product = system.records[product_code].product
    quantity = item_data["quantity"]
    price = item_data["price"]
    bill.add_item(product, quantity, price)
```

#### Total system load from a `.json` file

```python
@staticmethod
def load_full_backup(path, system):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
```
Here the JSON file containing the full system backup is opened. Now we continue with the methods after loading the JSON file.

<h4 align="left"> Opening the file and loading data </h4>

```python
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
```
This first block opens the JSON file containing the complete system backup, using the path provided in the `path` argument. The file content is loaded into memory via `json.load(f)` and stored in the variable `data` as a Python dictionary. This dictionary will contain keys such as `"customers"`, `"suppliers"`, `"records"`, `"movements"`, and `"bills"` which will be used to reconstruct the system components.

<h4 align="left"> Customer load </h4>

```python
for customer in data["customers"]:
    system.add_customer(Extracts.dict_to_customer(customer))
```
Then, the customers are reconstructed. To do this, each element in the `data["customers"]` list, representing serialized customer data, is iterated over. Each entry is transformed into a `Customer` object using the helper method `dict_to_customer`, and then added to the system via `system.add_customer()`. This recovers all customers registered before export.

<h4 align="left"> Supplier load </h4>

```python
for supplier in data["suppliers"]:
    existing = next(
        (
            x for x in system.suppliers.values() 
            if x.name == supplier["name"] 
            and x.contact_number == supplier["contact_number"]
        ), None
    )
    if not existing:
        system.add_supplier(Extracts.dict_to_supplier(supplier))
```
For suppliers, an additional step is performed: before adding a new supplier to the system, it checks if one already exists with the same name and contact number. If no duplicate supplier is found, the `Supplier` object is reconstructed from the dictionary using `dict_to_supplier` and added to the system. This prevents creating multiple entries for the same supplier during restoration.

<h4 align="left"> Inventory records upload </h4>

```python
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
```
This block restores all inventory records. If the product already exists in the system (verified by its code), its movement history is compared. The goal is to avoid duplicating already recorded movements, for which a unique key is generated for each movement (product, quantity, actor, and date). If any new movement is not in the existing ones, it is added to the history. If the product did not previously exist in the system, the complete record is reconstructed with `dict_to_inventory_record` and added as a new item.

<h4 align="left"> Location synchronization </h4>

```python
Location.sync_from_inventory(system.records.values())
```
Once all inventory records are loaded, the physical locations of the products are synchronized. The `sync_from_inventory` method ensures that each product is correctly assigned to its shelf and aisle within the system. This synchronization is important because the location may be necessary for physical inventory management in the real world.

<h4 align="left"> Movements load </h4>

```python
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
            stock._record.append(movement1)
```
Here the movement history of products, both incoming and outgoing, is restored. First, each JSON entry is transformed into a `Movement` object and added to the system. Then, that movement is associated with the corresponding stock history, verifying that it is not already registered to avoid duplicates. This step ensures that the complete operation history is available for future queries or audits, without affecting the current stock (hence `apply_stock=False`).

<h4 align="left"> Invoice upload </h4>

```python
for bill_data in data.get("bills", []):
    bill = Extracts.dict_to_bill(bill_data, system)
    system.bills[bill._bill_id] = bill
```
This block is responsible for restoring all invoices in the system. Each invoice in JSON format is converted into a `Bill` object using `dict_to_bill`, which reconstructs both the entity (customer or supplier) and the payment method, the items purchased or sold, and the date. Then, the invoice is added to the system using its unique identifier `_bill_id`, ensuring that economic transactions are recorded accurately.

<h4 align="left"> Association between movements and invoices </h4>

```python
for m in system.movements:
    for item in bill.items:
        if (m.product._code == item.product._code
            and m.amount == item.quantity
            and m.actor._id == bill.entity._id):
            m._bill_id = bill._bill_id
            break

```
Finally, the relationship between inventory movements and the invoices they belong to is established. For each movement, its product, quantity, and actor are compared with the items within each invoice. If a match is found, the movement is assigned the corresponding invoice ID. This step allows, for example, an outgoing movement to be traced back to a specific sale, which is essential for traceability and administrative control.


<h3 align="left"> generatePDF </h3>

First, the classes and their methods are defined:

<h4 align="left"> Class PDF </h4>

```python
class PDF(FPDF):
    def __init__(self, title="Report"):
        super().__init__()
        self.title = title
```
The base class `PDF` is defined, inheriting from `FPDF`, which allows building PDF files in Python. In its constructor (`__init__`), the parent class is initialized with `super().__init__()` and the title to be displayed in the document header is stored, defaulting to `"Report"`.

```python
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, self.title, ln=True, align="C")
        self.set_font("Helvetica", "", 10)
        self.cell(
            0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}",
            ln=True, align="C"
        )
        self.ln(5)
```
This method defines the PDF header. First, it sets a bold Helvetica font at size 14 and writes the centered title. Then, with a smaller font (Helvetica 10), it prints the current date centered. A small vertical space of 5 units is left after the header.

```python
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
```
Here the footer is defined. The cursor is positioned 15 units from the bottom edge, an italic small font is selected, and the current page number is printed centered.

```python
    def setup_page(self):
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
```
This method helps configure the page by enabling automatic page breaks with a bottom margin of 15 units and adding a new page.

```python
    def _add_table_header(self, headers, col_widths):
        self.set_font("Helvetica", "B", 10)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, align="C")
        self.ln()
```
This internal method creates the header row of a table. It uses a bold font and writes each header cell with borders and centered alignment, according to the width specified by `col_widths`.

```python
    def _add_table_row(self, row_data, col_widths, line_height=8):
        self.set_font("Helvetica", "", 10)
        for i, cell in enumerate(row_data):
            self.cell(col_widths[i], line_height, str(cell), border=1)
        self.ln()
```
This method adds a data row to the table. It uses a normal font and iterates over each value in the row to write it in a cell with the corresponding width and border.

```python
    def generate_table(self, headers, rows, col_widths):
        self._add_table_header(headers, col_widths)
        for row in rows:
            self._add_table_row(row, col_widths)
```
This method allows building a complete table by receiving headers, rows, and widths. It first writes the header row and then each data row.

<h4 align="left"> Class InventoryReportPDF </h4>

```python
class InventoryReportPDF(PDF):
    def __init__(self):
        super().__init__(title="Inventory Report")
```
This class inherits from `PDF` and represents an inventory report. In its constructor, it calls the base class (`PDF`) constructor with a custom title: `"Inventory Report"`, which will be shown in the header of each page.

```python
    def generate(self, records, filename="inventory_report.pdf"):
        self.setup_page()
        headers = [
            "Code", "Name", "Category", "Stock",
            "Min", "Max", "Location", "State"
        ]
        col_widths = [15, 30, 25, 15, 15, 15, 35, 40]
        rows = []
```
The `generate` method is responsible for building the content of the PDF. It starts by setting up the page and then defines the column headers (`headers`) and their widths (`col_widths`). It also initializes an empty list `rows` to store each table row.

```python
        for record in records:
            product = record["product"]
            stock = record["stock"]
            location = record["location"]

            state_data = product["state"]
            if "expiration_date" in state_data:
                exp = state_data["expiration_date"]
                state_str = f"Expires: {exp[0]:04d}-{exp[1]:02d}-{exp[2]:02d}"
            elif "condition" in state_data:
                state_str = f"Condition: {state_data['condition']}"
            else:
                state_str = "Unknown"
```
It iterates over each record in `records`, extracting the product, its inventory information (`stock`), and its location. Then it checks if the product's state includes an expiration date or a specific condition, and builds the `state_str` string accordingly.

```python
            rows.append([
                product["code"],
                product["name"],
                product["category"],
                stock["actual_stock"],
                stock["minimum_stock"],
                stock["maximum_stock"],
                f"Aisle {location['aisle']} - Shelf {location['shelf']}",
                state_str
            ])
```
With all the processed information, it builds a list representing a row in the PDF table and adds it to `rows`.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
Finally, it calls the inherited `generate_table` method to build the table and saves the PDF file with the provided name (default is `inventory_report.pdf`).

<h4 align="left"> Class MovementsReportPDF </h4>

```python
class MovementsReportPDF(PDF):
    def __init__(self):
        super().__init__(title="Inventory Movements Report")
```
This class generates an inventory movements report. In its constructor, a specific title `"Inventory Movements Report"` is passed to the base class.

```python
    def generate(self, movements, filename="movements_report.pdf"):
        self.setup_page()
        headers = [
            "Date", "Type", "Product Code", 
            "Quantity", "Actor", "Reason"
        ]
        col_widths = [25, 10, 25, 20, 60, 50]
        rows = []
```
The `generate` method prepares the page and defines the column headers and widths. The `rows` list is also initialized to store the movements.

```python
        for movement in movements:
            rows.append([
                movement["Date"],
                movement["Type"],
                movement["Code"],
                movement["Quantity"],
                movement["Actor"],
                movement["Reason"]
            ])
```
It iterates over each movement and extracts the relevant information to add it as a new row in the table.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
The table is generated with the data and the PDF is saved under the specified name.


<h4 align="left"> Class BillPDF </h4>

```python
class BillPDF(PDF):
    def generate(self, bill, filename="bill_report.pdf"):
        self.add_page()
        self.set_font("Helvetica", "", 12)
```
This class also inherits from `PDF` and its purpose is to generate an invoice. Unlike others, it does not define its own constructor, so it uses the default title `"Report"`. In the `generate` method, it adds a new page and sets the base font for the document content.

```python
        self.cell(0, 10, f"Bill ID: {bill._bill_id}", ln=True)
        self.cell(0, 10, f"Date: {bill.date.strftime('%Y-%m-%d')}", ln=True)
        self.cell(0, 10, f"Entity: {bill.entity.name}", ln=True)
        self.cell(0, 10, f"Type: {bill.entity_type}", ln=True)
        self.cell(0, 10, f"Payment Method: {bill.payment_method}", ln=True)
```
Several basic invoice details are printed in the PDF: the ID, the date, the involved entity (customer or supplier), the entity type, and the payment method.

```python
        if isinstance(bill.payment_method, Cash):
            total = bill.calculate_total()
            given = bill.payment_method.cash_given
            if given >= total:
                change = given - total
                self.cell(
                    0, 10, f"Paid for: ${given:.2f} - Change: ${change:.2f}",
                    ln=True
                )
            else:
                lack = total - given
                self.cell(
                    0, 10, f"Cash Insuficient. Lack: ${lack:.2f}", ln=True
                )
```
If the payment method is cash (`Cash`), an additional check is performed. The invoice total and the amount given are calculated. If the amount is sufficient, the change to return is shown; otherwise, it indicates how much money is missing. This section provides extra control for cash payments.

```python
        self.ln(5)
```
A small vertical space is added before continuing with the products table.

```python
        self.set_font("Helvetica", "B", 10)
        headers = ["Code", "Product", "Amount", "Unit Cost", "Subtotal"]
        col_widths = [30, 50, 30, 30, 30]
        self._add_table_header(headers, col_widths)
```
A bold font is set for the table headers, then the inherited `_add_table_header` method is called to draw the headers with their respective widths.

```python
        self.set_font("Helvetica", "", 10)
        for item in bill.items:
            self._add_table_row([
                item.product._code,
                item.product.name,
                item.quantity,
                f"${item.price:.2f}",
                f"${item.quantity * item.price:.2f}"
            ], col_widths)
```
It switches to a normal font for the rows and iterates over the invoice products. For each one, it extracts the data and generates a row with code, name, quantity, unit price, and subtotal (quantity × price).

```python
        self.set_font("Helvetica", "B", 11)
        self.cell(sum(col_widths[:-1]), 10, "Total", border=1, align="R")
        self.cell(
            col_widths[-1], 10, f"${bill.calculate_total():.2f}",
            border=1, align="R"
        )
        self.ln()
        self.output(filename)
```
Finally, a row with the invoice total is added. It uses a cell that spans all columns except the last one (where the total value goes). Then, the document is saved as a PDF file with the specified name.

<h4 align="left"> Class CriticalStockPDF </h4>

```python
class CriticalStockPDF(PDF):
    def __init__(self):
        super().__init__(title="Critic Stock")
```
This class inherits from `PDF` and is used to generate a report of products whose stock is in a critical state (below the minimum). In the constructor, it calls the base class (`PDF`) and sets the title to `"Critic Stock"`, which will be shown in the PDF header.

```python
    def generate(self, records: list, filename="critical_stock.pdf"):
        self.add_page()
```
The `generate` method takes as arguments a list of `records` (products in critical state) and the filename to generate. It starts by adding a new page to the PDF document.

```python
        headers = [
            "Code", "Product", "Category", "Stock", "Minimum", "Location"
        ]
        col_widths = [20, 45, 30, 20, 25, 50]
```
The table headers to be shown in the report are defined, along with the corresponding widths for each column. The information includes the code, product name, category, current quantity, minimum stock, and location.

```python
        rows = []
        for record in records:
            product = record.product
            stock = record.stock
            location = record.location
```
The `rows` list is initialized to hold the data rows. Then, it iterates over each received record. It extracts the product, its stock information, and its location within the inventory.

```python
            rows.append([
                product._code,
                product.name,
                product.category,
                stock.get_actual_stock(),
                stock.minimum_stock,
                f"Aisle {location.aisle} - Shelf {location.shelf}"
            ])
```
A row is constructed with the product data: the code (accessed as a private attribute), name, category, current stock (using the `get_actual_stock()` method), minimum required, and the location formatted as "Aisle X - Shelf Y". Each row is added to the `rows` list.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
Finally, the `generate_table` method is called to render the complete table, using the defined headers, rows, and widths. Then, the PDF is saved with the provided name.

<h4 align="left"> Class ActorHistoryPDF </h4>

```python
class ActorHistoryPDF(PDF):
    def __init__(self, actor_name, actor_type):
        title = f"History for {actor_type.capitalize()}: {actor_name}"
        super().__init__(title)
```
This class inherits from `PDF` and is used to generate a history of movements made by a specific system actor (for example, a supplier or a user). In the constructor, it receives the `actor_name` and `actor_type`, and dynamically builds the report title in the format `"History for <ActorType>: <ActorName>"`. It then passes this title to the base `PDF` class to be used as the document header.

```python
    def generate(self, movements: list, filename="actor_history.pdf"):
        self.setup_page()
```
The `generate` method receives the list of movements to report and the output filename. It starts by initializing the PDF page with `setup_page()`.

```python
        headers = ["Date", "Product", "Code", "Amount", "Type", "Reason"]
        col_widths = [25, 45, 25, 15, 20, 60]
```
The table headers are defined: date, product name, code, quantity, movement type (in or out), and reason for the movement. The widths for each column in the PDF are also specified.

```python
        rows = []
        for movement in movements:
            rows.append([
                movement.date.strftime("%Y-%m-%d"),
                movement.product.name,
                movement.product._code,
                movement.amount,
                movement.type,
                movement.reason
            ])
```
The `rows` list is created to store each movement as a table row. For each `movement` object:

- The date is converted to `YYYY-MM-DD` format.

- The product name and its code (which is private) are accessed.

- The quantity involved (`amount`), movement type (`type`), and reason (`reason`) are recorded.

All these data are grouped into a row that is added to the table.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
Finally, `generate_table` is called to visually build the table in the PDF, and the file is saved with the specified name (`actor_history.pdf` by default).

<h4 align="left"> Class SalesSummaryPDF </h4>

```python
class SalesSummaryPDF(PDF):
    def __init__(self, title="Sales Summary Report"):
        super().__init__(title)
```
This class also inherits from `PDF` and is designed to generate a sales summary report. In the constructor, a custom title can be specified (default is `"Sales Summary Report"`). This title is passed to the base class `PDF` and will be automatically displayed in the document header.

```python
    def generate(self, summary_data: dict, filename="sales_summary.pdf"):
        self.setup_page()
```
The `generate` method takes as input a dictionary `summary_data` that contains the sales summary per product, and optionally a filename to save the PDF (`sales_summary.pdf` by default). It first sets up the page by calling `setup_page()`.

```python
        headers = [
            "Code", "Product", "IN Qty", "IN Cost", "OUT Qty", "OUT Sales"
        ]
        col_widths = [30, 50, 25, 30, 25, 30]
```
The table headers for the report are then defined. Each column represents:

- `Code`: the product code.

- `Product`: the product name.

- `IN Qty`: the total number of units added to inventory.

- `IN Cost`: the total cost of those entries.

- `OUT Qty`: the total number of units removed (sold or dispatched).

- `OUT Sales`: the value of those outputs.

The column widths are also defined so that they are proportionally and clearly distributed in the PDF.

```python
        rows = []
        for code, data in summary_data.items():
            rows.append([
                code,
                data["name"],
                str(data["in"]["qty"]),
                f"${data['in']['cost']:.2f}",
                str(data["out"]["qty"]),
                f"${data['out']['cost']:.2f}"
            ])
```
The table rows are built by iterating through the `summary_data` dictionary, where each key `code` represents a product. The associated values must include:

- The product name (`data["name"]`),

- The quantity and total cost of inputs (`data["in"]["qty"]` and `data["in"]["cost"]`),

- The quantity and value of outputs (`data["out"]["qty"]` and `data["out"]["cost"]`).

Monetary values are formatted to two decimal places using `f"${value:.2f}"`.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
Finally, the `generate_table` method is called to render the headers and rows in the PDF, and the file is saved with `self.output(filename)`.

<h3 align="left"> System </h3>

```python
from Inventory_System.Inventory_Management.inventory import Inventory
from Inventory_System.Inventory_Management.inventory_record import InventoryRecord
from Inventory_System.Inventory_Management.location import Location
from Inventory_System.Inventory_Management.stock import Stock
from Inventory_System.Transactions.movements import Movement
from Inventory_System.Transactions.bills import Bill
from Inventory_System.Operantions_Center.extracts import Extracts
from Inventory_System.Operantions_Center.generatepdf import (
    ActorHistoryPDF, BillPDF, CriticalStockPDF,
    InventoryReportPDF, MovementsReportPDF, SalesSummaryPDF
)
```
The file begins with a series of imports that bring in the necessary modules and classes for the system to function. These include the base class `Inventory`, the classes that model products, locations, stocks, and movements, as well as the components responsible for generating invoices, reports, and PDF extracts.


```python
class System(Inventory):
    def __init__(self):
        super().__init__()
        self.bills = {}
        self.customers = {}
        self.suppliers = {}
```
Then, the `System` class is defined, which inherits from `Inventory`. In its constructor (`__init__`), the base class initializer is called using `super()`, and three empty dictionaries are created: `bills`, `customers`, and `suppliers`. These will store the registered invoices, customers, and suppliers respectively.

```python
    def entry_record(self, product, amount, supplier, reason):
        code = product._code
        if code in self.records:
            raise ValueError(f"Product code {code} is already in inventory.")
        
        location = Location.assign_location(product.category, product._code)
        stock = Stock(0, 20, 200)
        record = InventoryRecord(product, stock, location)
        self.add_record(record)
        movement = Movement(product, amount, supplier, reason)
        self.add_movement(movement)
        print(f"Product {product.name} added at {location.to_dict()}")
```
The `entry_record` method allows registering a new product in the inventory. It first checks if the product already exists; if not, it assigns an automatic location based on its category, creates a `Stock` object, wraps everything in an `InventoryRecord`, and adds it to the system. The entry movement is also recorded using `Movement`.


```python
    def make_sale(self, product_code, amount, customer, reason):
        if product_code not in self.records:
            raise ValueError("Product code not found in inventory.")
        
        record = self.records[product_code]
        movement = Movement(record.product, amount, customer, reason)
        delta = movement.get_delta()
        stock = record.stock

        if not stock.is_valid_update(delta):
            print(
                f"Movement for {record.product.name} failed due "
                  "to insufficient stock."
            )
            return False

        self.add_movement(movement) 
        print(f"Movement for {record.product.name} recorded successfully.")
        return True
```
The `make_sale` method handles a sale. It checks that the product exists, retrieves the inventory record, and creates an output movement. Before executing it, it verifies that there is enough available stock. If the validation passes, the movement is added.

```python
    def add_customer(self, customer):
        if customer._id in self.customers:
            print(f"Customer '{customer.name}' already exists.")
        else:
            self.customers[customer._id] = customer
            print(f"Customer '{customer.name}' added.")

    def add_supplier(self, supplier):
        if supplier._id in self.suppliers:
            print(f"Supplier '{supplier.name}' already exists.")
        else:
            self.suppliers[supplier._id] = supplier
            print(f"Supplier '{supplier.name}' added.")
```
The `add_customer` and `add_supplier` methods allow registering new actors in the system. They verify whether the customer or supplier ID already exists, and if not, they are added.

```python
    def generate_customer_history(self, customer_id):
        if customer_id not in self.customers:
            raise ValueError(f"Customer not found")
        return [
            movement.to_dict() for movement in self.movements
                if (
                    movement._actor_id == customer_id and 
                    movement.actor_type == "customer"
                )
        ]
        
    def generate_supplier_history(self, supplier_id):
        if supplier_id not in self.suppliers:
            raise ValueError(f"Supplier not found")
        return [
            movement.to_dict() for movement in self.movements
                if (movement._actor_id == supplier_id 
                    and movement.actor_type == "supplier"
                )
        ]
```
The `generate_customer_history` and `generate_supplier_history` methods allow obtaining a list of movements associated with a customer or supplier. They filter the registered movements based on the actor’s ID and type.

```python
    def create_bill(self, entity, movements, payment_method):
        bill = Bill(entity, payment_method)

        for movement in movements:
            if movement.actor._id != entity._id:
                raise ValueError("Movement does not belong to this entity.")

            sale_price = movement.final_price
            bill.add_item(
                movement.product,
                movement.amount,
                sale_price
            )
            movement._bill_id = bill._bill_id

        self.bills[bill._bill_id] = bill

        total = bill.calculate_total()
        if not payment_method.pay(total):
            print("Payment failed.")
            return None

        print(f"Bill {bill._bill_id} created for {entity.name}.")
        return bill
```
The `create_bill` method generates an invoice from a list of movements. It verifies that the movements belong to the same actor, adds the products to the `Bill` object, and stores its reference. Finally, it attempts to process the payment using the corresponding payment method.

```python
    def export_full_system(self, path="full_backup.json"):
        Extracts.export_full_system(self, path)

    def load_full_backup(self, path="full_backup.json"):
        Extracts.load_full_backup(path, self)
```
The `export_full_system` and `load_full_backup` methods allow exporting or importing a full system backup to a `.json` file, using the `Extracts` class.

```python
    def export_inventory_pdf(self, filename="inventory_report.pdf"):
        data = [r.to_dict() for r in self.records.values()]
        pdf = InventoryReportPDF()
        pdf.generate(data)
        pdf.output(filename)

    def export_movements_pdf(self, filename="movements_report.pdf"):
        data = [movement.to_dict() for movement in self.movements]
        pdf = MovementsReportPDF()
        pdf.generate(data)

    def export_bill_pdf(self, bill_id: str, filename="bill_report.pdf"):
        try:
            bill = self.bills.get(bill_id)
            if not bill:
                raise ValueError(f"Bill ID {bill_id} not found.")
            
            if not filename.lower().endswith(".pdf"):
                filename += ".pdf"

            pdf = BillPDF()
            pdf.generate(bill, filename)
            print(f"Bill exported: {filename}")

        except Exception as e:
            print(f"Error generating PDF Bill: {e}")
```
Next are the methods used to generate various types of PDF reports. For example, `export_inventory_pdf` generates an inventory report, `export_movements_pdf` generates a movements report, and `export_bill_pdf` generates an individual invoice.

```python
    def export_critical_stock_pdf(self, filename="critical_stock.pdf"):
        critical = super().get_critical_records()
        if not critical:
            print("No hay stocks críticos.")
            return False
        pdf = CriticalStockPDF()
        pdf.generate(critical, filename)
        return True
```
The `export_critical_stock_pdf` method generates a report of products that are below their minimum stock level. If there are no critical products, a message is printed.

```python
    def export_actor_history_pdf(self, actor_id: str, filename=None):
        try:
            actor = (
                self.customers.get(actor_id) or 
                self.suppliers.get(actor_id)
            )
            if not actor:
                raise ValueError(f"No actor found with ID {actor_id}")

            actor_type = (
                "customer" if actor_id in self.customers else "supplier"
            )
            actor_name = actor.name

            filtered_movements = [
                m for m in self.movements if m._actor_id == actor_id
            ]

            if not filtered_movements:
                print(f"No movements found for {actor_type} '{actor_name}'.")
                return

            if not filename:
                filename = (
                    f"{actor_type}_{actor_name.replace(' ', '_')}_history.pdf"
                )

            pdf = ActorHistoryPDF(actor_name, actor_type)
            pdf.generate(filtered_movements, filename)
            print(f"History PDF generated: {filename}")

        except Exception as e:
            print(f"Error generating actor history PDF: {e}")
```
The `export_actor_history_pdf` method generates a movement history for an actor (customer or supplier). It detects the actor's type, filters the movements, and generates the corresponding PDF.

```python
    def export_sales_summary_pdf(
        self, filename="sales_summary.pdf", product_code=None
    ):
        try:
            movements = self.movements
            if product_code:
                movements = [
                    m for m in movements if m.product._code == product_code
                ]

            if not movements:
                print("There're no data to make a report.")
                return

            summary = {}
            for m in movements:
                code = m.product._code
                if code not in summary:
                    summary[code] = {
                        "name": m.product.name,
                        "in": {"qty": 0, "cost": 0.0},
                        "out": {"qty": 0, "cost": 0.0}
                    }

                if m.type == "in":  # Compras
                    summary[code]["in"]["qty"] += m.amount
                    summary[code]["in"]["cost"] += m.amount * m.product._price
                else:  # Salidas (ventas)
                    summary[code]["out"]["qty"] += m.amount
                    summary[code]["out"]["cost"] += m.amount * m.final_price

            title = f"Resumen de Ventas y Compras"
            if product_code:
                title += (
                    f" - Producto: {summary[product_code]['name']} "
                    f"({product_code})"
                )

            pdf = SalesSummaryPDF(title)
            pdf.generate(summary, filename)
            print(f"Resumen generado en: {filename}")

        except Exception as e:
            print(f"Error generando el resumen: {e}")
```
Finally, the `export_sales_summary_pdf` method generates a sales and purchase summary, showing entries (purchases) and outputs (sales) for each product. It can be filtered by product code.









---------

We import the `tkinter` library as `tk`, and from it we also import the modules `filedialog`, `messagebox`, `Toplevel`, `StringVar`, `OptionMenu`, and `ttk`.

```python
import tkinter as tk
from tkinter import (
    filedialog, messagebox, Toplevel, StringVar, OptionMenu, ttk
)
```

<h3 align="left"> App </h3>

De los distintos módulos de `Inventory_System`, importamos las clases `System`, `Extracts`, `Product`, `State`, `Supplier`, `Customer`, `Bill`, `Card`, `Cash` y `Movement`.

```python 
from Inventory_System.Operantions_Center.system import System
from Inventory_System.Operantions_Center.extracts import Extracts
from Inventory_System.Products.product import Product
from Inventory_System.Products.state import State
from Inventory_System.People.supplier import Supplier
from Inventory_System.People.customer import Customer
from Inventory_System.Transactions.bills import Bill
from Inventory_System.Transactions.payment import Card, Cash
from Inventory_System.Transactions.movements import Movement
```

Creamos una clase `InventoryApp`, en la cual vamos a definir absolutamente todo lo que tiene que ver con la interfaz grafica (GUI). Definimos el constructor `__init__` con las instancias `root` y `system`, y le damos el título `Inventory Management System` a nuestra aplicación. También especificamos el estilo a usar y las margenes de la interfaz.

```python
class InventoryApp:
    def __init__(self, root, system):
        self.root = root
        root.title("Inventory Management System")
        self.system = system

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)
```

Definimos los botones que va a tener la interfaz principal, y que función va a tener cada uno de estos al ser presionado.

```python
        buttons = [
            ("📂 Load JSON archive", self.load_json),
            ("💾 Export to JSON archive", self.export_to_json),
            ("➕ Add Product", self.add_product_method),
            ("📋 Inventory Report", self.generate_inventory_pdf),
            ("🔄 Add Movement", self.add_movement_method),
            ("🧾 Cash Register", self.create_bill_method),
            ("📋 Generate movements report", self.export_movements_report),
            ("📜 Customer/Supplier History", self.generate_actor_history),
            ("📤 Export Bill", self.export_bill),
            ("📈 Sales Summary", self.generate_sales_summary),
            ("📦 Restock Suggestions", self.show_restock_suggestions),
            ("🚪 Quit", root.quit)
        ]
```

Para crear un botón, es necesario mandarle los parámetros `main_frame`, `text` y `command`, es decir, que tamaño va a tener cada botón, que va a decir cada uno, y que función va a tener. Se especifican las márgenes y se hace posible ajustar el texto al expandir la interfaz.

```python
        for i, (text, command) in enumerate(buttons):
            ttk.Button(
                main_frame, text=text, command=command
            ).pack(pady=6, fill="x")
```

Definimos la función `load_json`, la cual vamos a utilizar para cargar el archivo .JSON donde vamos a tener las bibliotecas de datos. Este nos va a permitir abrir el explorador de archivos para añadir nuestro archivo especificamente .JSON. Si la ruta del archivo es correcta, se hara backup correctamente y aparecerá un messagebox con el mensaje `"Success", "JSON archive has been loaded"`. En caso de que salga un error, el mensaje sera `"Error", "Couldn't load the archive"` y nos especificara el tipo de error ocurrido.

```python
    def load_json(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")]
        )
        if filepath:
            try:
                System.load_full_backup(self.system, filepath)
                messagebox.showinfo(
                    "Success", "JSON archive has been loaded."
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Couldn't load the archive:\n{e}"
                )
```

La función `generate_inventory_pdf` es definida para exportar el reporte de inventario como un archivo .PDF y guardarlo en la carpeta designada. Esto lo hara con el metodo `export_inventory_pdf` que viene del modulo `System`. En caso de que la exportación sea exitosa, aparecerá un messagebox con el mensaje `"Success", "Report has been generated as 'inventory_report.pdf'"`. En caso de que haya ocurrido un error, el mensaje será `"Error", "Couldn't generate the report"`, y especificara el error ocurrido.

```python
    def generate_inventory_pdf(self):
        try:
            System.export_inventory_pdf(self.system)
            messagebox.showinfo(
                "Success", 
                "Report has been generated as 'inventory_report.pdf'"
            )
        except Exception as e:
            messagebox.showerror(
                "Error", f"Couldn't generate the report:\n{e}"
            )
```

Definimos la función `generate_actor_history` para generar y exportar el historial ya sea de los clientes o de los proveedores. Este generará una ventana donde nos pedira ingresar el ID del correspondiente actor. Si el ID ingresado es correcto, entonces aparecerá el mensaje `"Success", "History has been generated"`. En caso de que no sea correcto, no retornará nada. En caso de que ocurra un error, el mensaje será `"Error", "Couldn't generate the history"`, y especificara el error ocurrido.

```python
    def generate_actor_history(self):
        actor_id = simple_input_dialog(
            "Join the actor ID (customer/supplier):"
        )
        if not actor_id:
            return
        try:
            System.export_actor_history_pdf(self.system, actor_id)
            messagebox.showinfo("Success", f"History has been generated.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Couldn't generate the history:\n{e}"
            )
```

Definimos la función `add_product_method` para poder agregar un producto manualmente al inventario. Este generará una ventana emergente con titulo `Add Product`, de la cual definimos el tamaño de la interfaz, margenes, expansión, etc. Definimos los campos (`Fields`) que va a tener la ventana, que son `Name`, `Category`, `Code`, `Price` y `Initial Amount`.

```python
    def add_product_method(self):
        dialog = Toplevel(self.root)
        dialog.title("Add Product")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)

        fields = ["Name", "Category", "Code", "Price", "Initial Amount"]
        entries = {}
```

Para cada campo definido, se va a generar un cuadro de texto (`Label`) donde el usuario va a poder ingresar los valores correspondientes a su campo (`entries`), y lo que se ingrese en estos campos se va a guardar como una entrada (`entry`).

```python
        for field in fields:
            ttk.Label(
                main_frame, text=field).pack(padx=10, pady=2, anchor="w"
            )
            entry = ttk.Entry(main_frame)
            entry.pack(padx=10, pady=2, fill="x")
            entries[field] = entry
```

Se generará tambien otro campo llamado `"Select State type:"` en donde se crearán dos botones llamados `State` y `Expiration Date`. De estos solo se podra elegir uno a la vez, y nos permitirán ingresar el estado del producto al momento de ser ingresado al inventario, ya sea su estado fisico, o su fecha de vencimiento según corresponda. Estos valores se almacenaran con las claves `condition` y `date` respectivamente.

```python
        ttk.Label(
            main_frame, text="Select State type:"
        ).pack(pady=5, anchor="w")
        state_type = tk.StringVar(value="condition")
        ttk.Radiobutton(
            main_frame, text="State", variable=state_type, value="condition"
        ).pack(anchor="w")
        ttk.Radiobutton(
            main_frame, text="Expiration Date", 
            variable=state_type, value="date"
        ).pack(anchor="w")
```

Según el estado seleccionado, se generaran espacios para ingresar los datos de condición del producto. En caso de que el estado a ingresar sea la condición actual, se generará un cuadro de texto donde podremos ingresar el estado del producto.

```python
        state_container = ttk.Frame(main_frame)
        state_container.pack(pady=5, fill="x")

        condition_frame = ttk.Frame(state_container)
        ttk.Label(condition_frame, text="Condition:").pack(pady=2, anchor="w")
        condition_entry = ttk.Entry(condition_frame)
        condition_entry.pack(pady=2, fill="x")
```

Si el estado a ingresar es la fecha de expiración del producto, se generarán tres espacios de texto llamados `Exp. Year`, `Exp. Month` y `Exp. Day`, donde ingresaremos el año, mes y dia de expiracion del producto respectivamente.

```python
        expiration_frame = ttk.Frame(state_container)
        for label_text in ["Exp. Year:", "Exp. Month:", "Exp. Day:"]:
            ttk.Label(
                expiration_frame, text=label_text
            ).pack(pady=2, anchor="w")
            ttk.Entry(expiration_frame).pack(pady=2, fill="x")
        year_entry, month_entry, day_entry = (
            expiration_frame.winfo_children()[1::2]
        )
```

Se define la función `update_state_fields()` para que, en caso de que elijamos ingresar la condición del producto, el menú de fechas de vencimiento se oculte, y viceversa.

```python
        def update_state_fields():
            if state_type.get() == "condition":
                expiration_frame.pack_forget()
                condition_frame.pack(fill="x")
            else:
                condition_frame.pack_forget()
                expiration_frame.pack(fill="x")

        update_state_fields()
        state_type.trace_add("write", lambda *args: update_state_fields())
```

Se generará tambien un campo llamado `Select Supplier type:`, donde, por medio de dos botones (donde solo se puede elegir uno) vamos a elegir entre dos opciones: Existente `Existent` (`existent`) y nuevo `New` (`new`), para buscar proveedores ya existentes o para ingresar los datos de un nuevo proveedor respectivamente.

```python
        ttk.Label(
            main_frame, text="Select Supplier type:"
        ).pack(pady=5, anchor="w")
        supplier_option = tk.StringVar(value="existent")
        ttk.Radiobutton(
            main_frame, text="Existent", 
            variable=supplier_option, value="existent"
        ).pack(anchor="w")
        ttk.Radiobutton(
            main_frame, text="New", variable=supplier_option, value="new"
        ).pack(anchor="w")

        supplier_container = ttk.Frame(main_frame)
        supplier_container.pack(fill="x")
```

En caso de que se elija la opción de elegir un proveedor existente, aparecerá un campo llamado `Select existent supplier:` y se generará con `ttk.OptionMenu` un widget donde nos aparecerán todos los proveedores existentes. Estos se tomarán del diccionario de proveedores  de `system.suppliers.values` y aparecerán uno por uno donde vamos a poder elegir a uno de ellos.

```python
        existing_supplier_frame = ttk.Frame(supplier_container)
        ttk.Label(
            existing_supplier_frame, text="Select existent supplier:"
        ).pack(anchor="w")
        supplier_var = tk.StringVar()

        if self.system.suppliers:
            supplier_names = [s.name for s in self.system.suppliers.values()]
            supplier_var.set(supplier_names[0])
            supplier_menu = ttk.OptionMenu(
                existing_supplier_frame, supplier_var,
                supplier_names[0],*supplier_names
            )
```

En caso tal de que aún no hayan proveedores registrados, aparecerá el mensaje `There's not suppliers`, y el menu de opciones se inhabilitará hasta que se registre uno.

```python
        else:
            supplier_var.set("There's not suppliers")
            supplier_menu = ttk.OptionMenu(
                existing_supplier_frame, supplier_var,
                "There's not suppliers"
            )
            supplier_menu.state(["disabled"])
        supplier_menu.pack(fill="x")
        existing_supplier_frame.pack(pady=5, fill="x")
```

Si se eligio la opción de añadir un nuevo proveedor, entonces se generarán dos campos llamados `New supplier name:` y `New supplier contact:`. Estos tendran espacios de texto donde se colocarán el nombre y el numero de contacto del nuevo proveedor respectivamente.

```python
        new_supplier_frame = ttk.Frame(supplier_container)
        for label in ["New supplier name:", "New supplier contact:"]:
            ttk.Label(new_supplier_frame, text=label).pack(anchor="w")
            ttk.Entry(new_supplier_frame).pack(fill="x", pady=2)
        new_supplier_name, new_supplier_contact = (
            new_supplier_frame.winfo_children()[1::2]
        )
```

Se define la función `toggle_supplier_frames()` para que, si se eligio escoger un proveedor existente, se oculte el menu de agregar un nuevo proveedor y viceversa.

```python
        def toggle_supplier_frames():
            if supplier_option.get() == "existent":
                new_supplier_frame.pack_forget()
                existing_supplier_frame.pack(pady=5, fill="x")
            else:
                existing_supplier_frame.pack_forget()
                new_supplier_frame.pack(pady=5, fill="x")

        supplier_option.trace_add(
            "write", lambda *args: toggle_supplier_frames()
        )
```

La función `submit` la usaremos para guardar el producto con todos los parametros dados en el diccionario de registros de `System`. Esta función primeramente verifica que cada uno de los campos de ingreso de datos no este vacia, es decir que todos los campos tengan algun valor en ellas. En caso de que alguno de los campos `name`, `category`, `code`, `prices_str` o `amount_str` no tenga valor alguno, va a retornar el mensaje de error `"All fields must be filled"`.

```python
        def submit():
            try:
                name = entries["Name"].get().strip()
                category = entries["Category"].get().strip()
                code = entries["Code"].get().strip()
                price_str = entries["Price"].get().strip()
                amount_str = entries["Initial Amount"].get().strip()

                if (
                    not name or not category or not code or
                    not price_str or not amount_str
                ):
                    raise ValueError("All fields must be filled")
```

Si todos los campos de texto tienen algun valor, entonces la función comienza a evaluar los campos uno por uno para manejar las diferentes excepciones que puedan tener estas por separado. Comienza con los campos `price` y `amount`, que se guardarán como variables `float` e `int` respectivamente. Si el precio o el monto son iguales o menores a 0, va a retornar el error `"Price and Amount must be bigger than zero"`. En caso de que en estos campos no se hayan ingresado valores numericos, va a retornar el error `"Price and Amount must be numeric"`.

```python
                try:
                    price = float(price_str)
                    amount = int(amount_str)
                    if price <= 0 or amount <= 0:
                        raise ValueError(
                            "Price and Amount must be bigger than zero"
                        )
                except ValueError:
                    raise ValueError("Price and Amount must be numeric.")
```

Luego, se evalua el campo `state_type`, donde si se escogio `"condition"`, se verifica que se haya llenado el campo, o si no retorna el error `"You must fill the condition"`.

```python
                if state_type.get() == "condition":
                    if (
                        not condition_entry or
                        not condition_entry.get().strip()
                    ):
                        raise ValueError("You must fill the codition.")
                    state = State(condition=condition_entry.get().strip())
```

En caso de que se haya escogido `expiration date`, tambien se verifica que todos los campos de la fecha hayan sido diligenciados, o retornara el error `"You must fill the entire date"`. Cuando se llenen todos los campos, se tomarán las entradas de los campos y se hará una tupla con ellos llamada `state`, donde se verificará que esten bien diligenciadas las fechas, pues, en caso de que no, retornara el ValueError `"Date fields must be valid numbers"`.

```python
                else:
                    if not year_entry or not month_entry or not day_entry:
                        raise ValueError("You must fill the entire date.")
                    try:
                        state_tuple = (
                            int(year_entry.get().strip()),
                            int(month_entry.get().strip()),
                            int(day_entry.get().strip())
                        )
                        state = State(expiration_date=state_tuple)
                    except ValueError:
                        raise ValueError(
                            "Date fields must be valid numbers."
                        )
```

Continuando con el campo de proveedores, en caso de que se haya elegido `existent`, se toman los proveedores del diccionario uno por uno y el objeto se guarda en la variable `supplier`. En caso de que se haya elegido `new`, se verifica que los campos `supplier_name` y `supplier contact` hayan sido diligenciados, en caso de que no, retorna el error `"You must enter the supplier name and contact"`. Se verifica tambien que el `supplier_contact` sea un valor numerico, y en caso de que no, retorna el mensaje `"The contact number must be numeric only"`.

```python
                if (
                    supplier_option.get() == "existent" and
                    self.system.suppliers
                ):
                    supplier = next(
                        (
                            s for s in self.system.suppliers.values() 
                            if s.name == supplier_var.get()
                         ), None
                    )
                else:
                    supplier_name = new_supplier_name.get().strip()
                    supplier_contact = new_supplier_contact.get().strip()
                    if not supplier_name or not supplier_contact:
                        raise ValueError(
                            "You must enter the supplier name and contact."
                        )
                    if not supplier_contact.isdigit():
                        raise ValueError(
                            "The contact number must be numeric only"
                        )
```

Si el proveedor es existente, se agrega a la variable `supplier`. Si no, a la variable `supplier` se le asignan los valores de `Supplier(supplier_name, supplier_contact)` y se añade a la biblioteca de proveedores por medio del metodo `system.add_supplier`.

```python
                    existing = [
                        supplier for supplier in self.system.suppliers.values() 
                        if (
                            supplier.name == supplier_name and
                            supplier.contact == supplier_contact
                        )
                    ]
                    if existing:
                        supplier = existing[0]
                    else:
                        supplier = Supplier(supplier_name, supplier_contact)
                        self.system.add_supplier(supplier)
```

A la variable `product` se le asignan los valores de `Product(name, category, code, price, state)` y se añaden a la biblioteca de registros junto con los datos de `product`, `amount`, `supplier` y `reason` que sera `"New add"`. Si el registro se realiza correctamente, se generará un messagebox con el mensaje `"Success", "Product added"` especificando el producto. En caso de que ocurra un error, se generará un messagebox con el mensaje `"Error", "Couldn't add the product"` y especificando el error ocurrido.

```python
                product = Product(name, category, code, price, state)
                self.system.entry_record(
                    product, amount, supplier, reason="New add"
                )
                messagebox.showinfo("Success", f"Product '{name}' added.")
                dialog.destroy()

            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror(
                    "Error", f"Couldn't add the product:\n{str(e)}"
                )
```

Finalmente, se genera un botón llamado `Add Product` con el comando `submit`, que va a enviar los datos a los diccionarios correspondientes y cerrará la ventana.

```python
        ttk.Button(
            main_frame, text="Add Product", command=submit
        ).pack(pady=10)
```

Definimos la función `export_to_json` para guardar el archivo .JSON con el nombre `"Save Backup"`. Si la ruta seleccionada por el usuario es correcta, se genera un messagebox con el mensaje `"Success", "Backup saved in:"` y especifica la ruta seleccionada. En caso de que ocurra algún error, se genera un messagebox con el mensaje `"Error", "Couldn't export"` y especificando el error ocurrido.

```python
    def export_to_json(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Backup"
        )
        if filepath:
            try:
                self.system.export_full_system(filepath)
                messagebox.showinfo(
                    "Success", f"Backup saved in:\n{filepath}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't export:\n{e}")
```

Definimos la función `add_movement_method` para añadir un movimiento a la biblioteca de movimientos. Si no hay productos existentes, el metodo generará un messagebox con el mensaje de error `"No products available", "Unable to register movements, no products availables"`.

```python
    def add_movement_method(self):
        if not self.system.records:
            messagebox.showwarning(
                "No products available", 
                "Unable to register movements, no products availables"
            )
            return
```

En caso de que si hayan productos, se procede a generar una ventana emergente llamada `Register Movement` donde se ingresarán todos los datos del movimiento. En dicha ventana habrá un campo llamado `Select Movement type:`, en el cual se generarán dos botones llamados `In` y `Out`, donde vamos a especificar si el movimiento que vamos a registrar es una entrada o una salida de productos respectivamente, y solo vamos a poder escoger uno u otro.

```python
        dialog = tk.Toplevel()
        dialog.title("Register Movement")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame, text="Select Movement type:"
        ).pack(pady=5, anchor="w")
        movement_type = tk.StringVar(value="in")
        ttk.Radiobutton(
            main_frame, text="In", variable=movement_type, value="in", 
            command=lambda: update_actor_menu()
        ).pack(anchor="w")
        ttk.Radiobutton(
            main_frame, text="Out", variable=movement_type, value="out", 
            command=lambda: update_actor_menu()
        ).pack(anchor="w")
```

Se generará tambien un campo llamado `Select product:` donde vamos a poder escoger uno de los productos que se encuentran en la biblioteca de productos `system.records.values` (se tomaran los nombres de los productos (`product.name`)). En este campo habrá un menu de opciones donde va a aparecer toda la lista de nombres de los productos uno por uno, donde vamos a poder escoger solo uno.

```python
        ttk.Label(main_frame, text="Select product:").pack(pady=5, anchor="w")
        product_var = tk.StringVar(main_frame)
        if self.system.records:
            product_var.set(
                next(iter(self.system.records.values())).product.name
            )
        product_menu = ttk.OptionMenu(
            main_frame, product_var, 
            *[record.product.name for record in self.system.records.values()]
        )
        product_menu.pack(pady=5, fill="x")
```

Otro de los campos que se habilitarán en esta ventana, es `Amount`, donde vamos a escribir en un cuadro de texto generado, la cantidad de unidades que vamos a añadir al movimiento.

```python
        ttk.Label(main_frame, text="Amount:").pack(pady=5, anchor="w")
        quantity_entry = ttk.Entry(main_frame)
        quantity_entry.pack(pady=5, fill="x")
```

El proximo campo generado en la pestaña es el de `Reason of the movement`, en el cual vamos a especificar en un cuadro de texto la descripcion del movimiento a generar.

```python
        ttk.Label(
            main_frame, text="Reason of the movement:"
        ).pack(pady=5, anchor="w")
        reason_entry = ttk.Entry(main_frame)
        reason_entry.pack(pady=5, fill="x")
```

Otro campo generado es `Type actor`, donde vamos a tener que escoger por medio de dos botones `Existent` y `New` si el movimiento es por medio de un actor ya existente o si queremos añadir uno nuevo al sistema respectivamente.

```python
        ttk.Label(main_frame, text="Type actor:").pack(pady=5, anchor="w")
        actor_option = tk.StringVar(value="existent")
        ttk.Radiobutton(
            main_frame, text="Existent", variable=actor_option, value="existent", 
            command=lambda: toggle_actor_fields()
        ).pack(anchor="w")
        ttk.Radiobutton(
            main_frame, text="New", variable=actor_option, value="new", 
            command=lambda: toggle_actor_fields()
        ).pack(anchor="w")

        actor_container = ttk.Frame(main_frame)
        actor_container.pack(pady=5, fill="x")
```

En el apartado de seleccionar un actor existente, se generara un campo llamado `Select existent actor`, donde, como lo dice el nombre, vamos a poder seleccionar el actor que vamos a registrar en el movimiento, esto por medio de un `OptionMenu` que va a contener todos los actores registrados en el sistema, del cual vamos a poder escoger solo uno.

```python
        existing_actor_frame = ttk.Frame(actor_container)
        actor_var = tk.StringVar(existing_actor_frame)
        actor_label = ttk.Label(
            existing_actor_frame, text="Select existent actor:"
        )
        actor_menu = ttk.OptionMenu(existing_actor_frame, actor_var, "")
        actor_label.pack(pady=5)
        actor_menu.pack(pady=5, fill="x")
```

En el apartado de `New` vamos a poder agregar al sistema el actor que vayamos a registrar en el movimiento. Esto por medio de dos campos generados llamados `New actor name` y `New actor contact/id`, donde podremos ingresar el nombre del actor y el numero de contacto o el numero de identificacion segun corresponda respectivamentre.

```python
        new_actor_frame = ttk.Frame(actor_container)
        new_actor_name_label = ttk.Label(
            new_actor_frame, text="New actor name:"
        )
        new_actor_contact_label = ttk.Label(
            new_actor_frame, text="New actor contact/id:"
        )
        new_actor_name_entry = ttk.Entry(new_actor_frame)
        new_actor_contact_entry = ttk.Entry(new_actor_frame)

        new_actor_name_label.pack(pady=3)
        new_actor_name_entry.pack(pady=3, fill="x")
        new_actor_contact_label.pack(pady=3)
        new_actor_contact_entry.pack(pady=3, fill="x")
```

Posteriormente definiremos la funcion `toggle_actor_fields` para que al momento de seleccionar tanto si es un actor existente o si vamos a agregar al nuevo actor, se muestren los campos correspondientes a cada eleccion, mientras que se ocultan los de la otra y viceversa.

```python
        def toggle_actor_fields():
            existing_actor_frame.pack_forget()
            new_actor_frame.pack_forget()

            if actor_option.get() == "existent":
                existing_actor_frame.pack(pady=5, fill="x")
            else:
                new_actor_frame.pack(pady=5, fill="x")
```

Definimos la funcion `update_actor_menu` para que, segun el tipo de movimiento que vamos a registrar, ya sea entrada `in` o salida `out`, se traigan los objetos de las bibliotecas de proveedores o de clientes respectivamente.

```python
        def update_actor_menu():
            if movement_type.get() == "in":
                options = [s.name for s in self.system.suppliers.values()]
            else:
                options = [c.name for c in self.system.customers.values()]

            for widget in existing_actor_frame.winfo_children():
                widget.destroy()
```

Estos objetos recolectados segun el tipo de movimiento, se mostraran en el menu de `OptionMenu` llamado `Select existent actor` donde vamos a poder escoger solo uno de estos. En caso de que no haya ningun actor registrado en el sistema, el `OptionMenu` generado se llamara `No actors available`, y en vez de desglosar un menu de opciones, dira el mensaje `No actors available`, y el menu estara desactivado. En caso de que todo este correcto, se ejecutara la funcion `update_actor_menu`.

```python
            ttk.Label(
                existing_actor_frame, text="Select existent actor:"
            ).pack(pady=2, anchor="w")

            if options:
                actor_var.set(options[0])
                new_menu = ttk.OptionMenu(
                    existing_actor_frame, actor_var, options[0], *options
                )
            else:
                actor_var.set("No actors available")
                new_menu = ttk.OptionMenu(
                    existing_actor_frame, actor_var, "No actors available"
                )
                new_menu.state(["disabled"])
            
            new_menu.pack(fill="x")
            toggle_actor_fields()

        update_actor_menu()
        actor_option.trace_add("write", lambda *args: toggle_actor_fields())
```

Para registrar el movimiento en el sistema, definimos la opcion `register_movement` que usaremos para registrar el movimiento , y en donde verificaremos que todos los campos, esten correctamente diligenciados. en el campo de `amount` debemos verificar que los valores ingresados sean un monto numerico, y que estos sean numeros positivos. Tambien en el campo de `reason of the movement` debe haberse ingresado alguna razon del movimiento.

```python
        def register_movement():
            try:
                if (
                    not quantity_entry.get().isdigit() or 
                    int(quantity_entry.get()) <= 0
                ):
                    raise ValueError("The amount must be positive.")
                if not reason_entry.get().strip():
                    raise ValueError("You have to enter a reason.")
```

Para cada producto del diccionario `system.records.values`, nos retorna un objeto `r`, y si el nombre (`r.product.name`) es igual al `product_name` que ingresamos, entonces se verifica que la cantidad del producto ingresada sea un valor entero positivo, y que el campo `reason` sea diligenciado.

```python
                product_name = product_var.get()
                product = next(
                    r.product for r in self.system.records.values() 
                    if r.product.name == product_name
                )
                cantidad = int(quantity_entry.get())
                reason = reason_entry.get().strip()
```

En caso de que en el tipo de movimiento hayamos especificado que es un ingreso de productos (`in`), entonces se verifica que, en caso tal de que hayamos escogido la opcion de un actor existente, este se encuentre registrado en el sistema. En caso de que no se encuentre el actor, retornara el mensaje de error `"The supplier selected is invalid"`.

```python
                if movement_type.get() == "in":
                    if actor_option.get() == "existent":
                        actor = next(
                            (
                                s for s in self.system.suppliers.values() 
                                if s.name == actor_var.get()
                             ), None
                        )
                        if not actor:
                            raise ValueError(
                                "The supplier selected is invalid."
                            )
```

Si escogimos que queremos añadir un nuevo actor al sistema, entonces se verificara que las entradas que hayamos colocado en los campos `name`, y `contact` hayan sido diligenciados. En caso de que no lo hayan sido, retornara el mensaje `"Enter the new supplier name and contact"`. Si todo esta diligenciado correctamente, se guardaran las entradas `name` y `contact` en un objeto llamado `actor`, el cual se mandara a los diccionarios del sistema.

```python
                    else:
                        name = new_actor_name_entry.get().strip()
                        contact = new_actor_contact_entry.get().strip()
                        if not name or not contact:
                            raise ValueError(
                                "Enter the new supplier name and contact."
                            )
                        actor = Supplier(name, contact)
                        self.system.add_supplier(actor)

                    self.system.restock(
                        product._code, cantidad, actor, reason
                    )
```

Ahora, en caso de que en el apartado de tipo de movimiento, hayamos escogido movimiento de tipo salida (`out`) y hayamos sleccionado la opcion `existent`, automaticamente se creara el objeto `actor`, en el cual vamos a traer cada uno de los objetos `c` en el diccionario de clientes del sistema `system.customers.values`. Cada uno de estos objetos se comparan con el nombre escogido, y si estos no concuerdan, retornara el mensaje `"The customer selected is invalid"`.

```python
                else:
                    if actor_option.get() == "existent":
                        actor = next(
                            (
                                c for c in self.system.customers.values() 
                                if c.name == actor_var.get()
                             ), None
                        )
                        if not actor:
                            raise ValueError(
                                "The customer selected is invalid."
                            )
```

En caso de que hayamos seleccionado la opcion `new` para registrar un nuevo cliente, entonces se verificara que los campos `name` y `contact` hayan sido diligenciados correctamente. En caso de que no, retornara el error `"Enter the new customer name and id"`. En caso de que esten bien diligenciados esos campos, se creara el objeto `actor`, al cual le asignaremos los atributos `name` y `contact` del objeto `Customer` traido de la biblioteca de clientes del sistema.

```python
                    else:
                        name = new_actor_name_entry.get().strip()
                        contact = new_actor_contact_entry.get().strip()
                        if not name or not contact:
                            raise ValueError(
                                "Enter the new customer name and id."
                            )
                        actor = Customer(name, contact)
                        self.system.add_customer(actor)

                    self.system.make_sale(
                        product._code, cantidad, actor, reason
                    )
```

Sea cual haya sido la opcion seleccionada, si esta fue procesada correctamente, entonces el sistema generara un messagebox con el mensaje `"Success", "Movement registered"`, y eliminara esta pestaña. En caso de que ocurra un error desconocido, generara un messagebox con el mensaje `"Error", "Couldn't register the movement"` y especifica el error ocurrido. 

```python
                messagebox.showinfo("Success", "Movement registered.")
                dialog.destroy()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Couldn't register the movement:\n{e}"
                )

        ttk.Button(
            main_frame, text="Register", command=register_movement
        ).pack(pady=15, fill="x")
```

Definimos la función `créate_bill_method`, la cual nos va a servir para crear una factura y exportarla al sistema en formato .PDF. Ya que los datos para crear la factura los traeremos del diccionario `system.records`, en caso de que este archivo no se encuentre o este vacio, se generara un messagebox con el mensaje `"No products available", "No registered products, it's not possible to create a bill"`

```python
    def create_bill_method(self):
        if not self.system.records:
            messagebox.showwarning(
                "No products available", 
                "No registered products, it's not possible to create a bill."
            )
            return
```

Se generara una ventana emergente titulada `Create a bill`, en donde el primer campo generado es `Select the actor type`, en el cual habran dos botones de seleccion para poder escoger el actor que se va a registrar en la factura entre cliente `Customer` o proveedor `Supplier`. Solo se podra escoger uno u otro.

```python
        dialog = tk.Toplevel(self.root)
        dialog.title("Create a bill")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=12)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Select the actor type:").pack(pady=5)
        actor_type = tk.StringVar(value="customer")
        ttk.Radiobutton(
            main_frame, text="Customer", variable=actor_type, 
            value="customer", command=lambda: update_actor_fields()
        ).pack()
        ttk.Radiobutton(
            main_frame, text="Supplier", variable=actor_type, 
            value="supplier", command=lambda: update_actor_fields()
        ).pack()
```

Luego de escoger el actor, se generan otro campo llamado `Choose actor: existing or new` donde vamos a escoger si vamos a usar un actor ya existente o vamos a registrar uno nuevo, esto por medio de los botones `Existent` y `New` respectivamente.

```python
        actor_mode = tk.StringVar(value="existent")
        ttk.Label(
            main_frame, text="Choose actor: existing or new?"
        ).pack(pady=5)
        ttk.Radiobutton(
            main_frame, text="Existent", variable=actor_mode, 
            value="existent", command=lambda: update_actor_fields()
        ).pack()
        ttk.Radiobutton(
            main_frame, text="New", variable=actor_mode, value="new", 
            command=lambda: update_actor_fields()
        ).pack()

        actor_frame = ttk.Frame(main_frame)
        actor_frame.pack(pady=10, fill="x")
        existing_actor_frame = ttk.Frame(actor_frame)
        new_actor_frame = ttk.Frame(actor_frame)

        actor_var = tk.StringVar()
        new_actor_name = None
        new_actor_contact = None
```

Definimos la funcion `update_actor_fields` para que, si vamos a escoger un actor existente, se oculten los apartados para registrar uno nuevo desde 0, y viceversa.

```python
        def update_actor_fields():
            for widget in existing_actor_frame.winfo_children():
                widget.destroy()
            for widget in new_actor_frame.winfo_children():
                widget.destroy()

            existing_actor_frame.pack_forget()
            new_actor_frame.pack_forget()
```

Se crea un objeto llamado `actors_dict`, al cual le vamos a asignar los datos del diccionario de los clientes, en caso de que se haya escogido al cliente como actor, o del diccionario de los proveedores, en caso de que se haya escogido al proveedor como actor.

```python
            actors_dict = (
                self.system.customers 
                if actor_type.get() == "customer" else self.system.suppliers
            )
```

Si se escogio la opcion de usar un actor existente, entonces se generara un campo llamado `Select an existent actor`, en donde se tomara el objeto creado `actors_dict`, y por cada uno de los valores contenidos en este, retornara un objeto `a` que posteriormente aparecera en un OptionMenu en donde vamos a poder escoger solo uno de estos.

```python
            if actor_mode.get() == "existent":
                existing_actor_frame.pack()
                ttk.Label(
                    existing_actor_frame, text="Select an existent actor:"
                ).pack()
                if actors_dict:
                    actor_names = [a.name for a in actors_dict.values()]
                    actor_var.set(actor_names[0])
                    actor_menu = ttk.OptionMenu(
                        existing_actor_frame, actor_var, 
                        actor_names[0], *actor_names
                    )
```

En caso de que los diccionarios tanto de clientes como de proveedores en el sistema se encuentren vacios, entonces el menu de OptionMenu aparecera vacio, tendra el mensaje `"No actors available"`, y este sera desactivado hasta que haya al menos un actor para seleccionar.

```python
                else:
                    actor_var.set("No actors available")
                    actor_menu = ttk.OptionMenu(
                        existing_actor_frame, actor_var, "No actors available"
                    )
                    actor_menu.state(["disabled"])
                actor_menu.pack()
```

Si se escogio añadir un nuevo actor desde 0, entonces el campo generado tendra dos cuadros de texto llamados `New actor name` y `New actor contact/id`, en donde colocaremos los datos de nombre y numero de contacto o numero de id del actor a registrar segun corresponda respectivamente. Finalmente, sea cual haya sido la eleccion, se ejecutara la funcion.

```python
            else:
                new_actor_frame.pack()
                ttk.Label(new_actor_frame, text="New actor name:").pack()
                nonlocal_new_name = ttk.Entry(new_actor_frame)
                nonlocal_new_name.pack(fill="x")
                ttk.Label(
                    new_actor_frame, text="New actor contact/id:"
                ).pack()
                nonlocal_new_contact = ttk.Entry(new_actor_frame)
                nonlocal_new_contact.pack(fill="x")

                nonlocal new_actor_name, new_actor_contact
                new_actor_name = nonlocal_new_name
                new_actor_contact = nonlocal_new_contact

        update_actor_fields()
```

Luego de esto, se generara un campo llamado `Add products` del que derivan dos campos llamados `Code` y `Amount`, en donde tendremos que ingresar el codigo del producto deseado y la cantidad que se va a poner en la factura respectivamente. Estos dos datos los guardaremos en objetos llamados `code_entry` y `qty_entry`. Tambien crearemos una lista vacia llamada `items`.

```python
        ttk.Label(main_frame, text="Add products:").pack(pady=4)
        manual_frame = ttk.Frame(main_frame)
        manual_frame.pack(pady=4)

        ttk.Label(manual_frame, text="Code:").grid(row=0, column=0)
        code_entry = ttk.Entry(manual_frame)
        code_entry.grid(row=0, column=1)

        ttk.Label(manual_frame, text="Amount:").grid(row=0, column=2)
        qty_entry = ttk.Entry(manual_frame)
        qty_entry.grid(row=0, column=3)

        items = []
```

Al objeto `columns` le asignaremos `Product`, `Amount` y `Price`, y definiremos el objeto `tree`, que sera un formato Treeview, definido por las columnas en `columns`.

```python
        columns = ("Product", "Amount", "Price")
        tree = ttk.Treeview(
            main_frame, columns=columns, show="headings", height=7
        )
```

Para cada columna en `columns`, se asignara el nombre de cada una como titulo de dicha columna en el Treeview. Es decir que en el Treeview habran tres columnas llamadas `Product`, `Amount` y `Price`.

```python
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(pady=8)
```

Definimos la funcion `add_manual_item` para añadir a la factura los items que esta va a tener de forma manual. En los objetos `code` y `qty` guardaremos los datos tomados en `code_entry` y `qty_entry` respectivamente. Si alguno de estos no ha sido diligenciado previamente, se generara un messagebox con el mensaje `"Error", "Complete all the fields"`. Si el codigo del producto `code` no se encuentra previamente registrado en el diccionario de registros del sistema, el messagebox generado tendra el mensaje `"Error", "Product x has not found in inventory"` especificando el codigo del producto que no se encuentra. Finalmente se verifica que la cantidad especificada del producto `qty` sea un numero entero, y en caso de que no, el messagebox tendra el mensaje `"Error", "Amount must be numeric"`.

```python
        def add_manual_item():
            code = code_entry.get().strip()
            qty = qty_entry.get().strip()
            if not code or not qty:
                messagebox.showerror("Error", "Complete all the fields.")
                return
            if code not in self.system.records:
                messagebox.showerror(
                    "Error", f"Product {code} has not found in inventory."
                )
                return
            try:
                qty = int(qty)
            except ValueError:
                messagebox.showerror("Error", "Amount must be numeric.")
                return

            product = self.system.records[code].product
            price = product._price
            items.append((product, qty))
            tree.insert("", "end", values=(product.name, qty, price))
            code_entry.delete(0, tk.END)
            qty_entry.delete(0, tk.END)
```

Al final de estos campos habra un boton llamado `Add`, el cual hara que la funcion `add_manual_item` se realice siempre y cuando todos los parametros hayan sido diligenciados correctamente.

```python
        ttk.Button(
            manual_frame, text="Add", command=add_manual_item
        ).grid(row=0, column=6, padx=5)
```

Abajo del Treeview habra un campo llamado `Pending Movements`, en el cual veremos los movimientos ya registrados en el sistema que estan pendientes por ser pagados. Este campo generara una Listbox en donde apareceran todos y cada uno de los pagos pendientes. Se crea una lista vacia llamada `pending_movements`.

```python
        ttk.Label(main_frame, text="Pending Movements:").pack(pady=5)
        pending_listbox = tk.Listbox(
            main_frame, selectmode=tk.EXTENDED, width=70, height=4
        )
        pending_listbox.pack()

        pending_movements = []
```

Definimos la funcion `update_pending_movements` para que, dependiendo del actor seleccionado ya sea cliente o proveedor, se muestren todos los movimientos pendientes que tienen estos, y se muestren en la listbox uno por uno.

```python
        def update_pending_movements():
            nonlocal pending_movements
            pending_listbox.delete(0, tk.END)

            actors_dict = (
                self.system.customers 
                if actor_type.get() == "customer" else self.system.suppliers
            )

            actor_obj = next((a for a in actors_dict.values() 
                            if a.name == actor_var.get()), None)

            if actor_obj:
                pending_movements = [
                    m for m in self.system.movements
                    if m.actor == actor_obj and 
                    getattr(m, "bill_id", None) is None
                ]
                for idx, mov in enumerate(pending_movements):
                    text = (
                        f"{idx+1}. {mov.product.name} x{mov.amount} — "
                        f"{mov.date.strftime('%Y-%m-%d')}"
                    )
                    pending_listbox.insert(tk.END, text)
            else:
                pending_movements = []

        actor_var.trace_add("write", lambda *args: update_pending_movements())
        update_pending_movements()
```

Abajo de esto, se generara otro campo llamado `Payment Method` del que derivaran dos botones llamados `Cash` y `Card`, en el cual especificaremos el metodo de pago que vamos a añadir a la factura, ya sea dinero en efectivo, o por tarjeta respectivamente. Por defecto, las entradas de ambos metodos de pago se definen como `None` hasta que se agregue alguno luego.

```python
        ttk.Label(main_frame, text="Payment Method:").pack(pady=5)
        payment_method = tk.StringVar(value="cash")
        ttk.Radiobutton(
            main_frame, text="Cash", variable=payment_method, value="cash"
        ).pack()
        ttk.Radiobutton(
            main_frame, text="Card", variable=payment_method, value="card"
        ).pack()

        payment_frame = ttk.Frame(main_frame)
        payment_frame.pack(pady=5)

        payment_frame.cash_entry_ = None
        payment_frame.card_entry_ = None
```

Definimos la funcion `update_payment_fields` para que, en caso de que hayamos escogido dinero en efectivo como metodo de pago, se genere un campo llamado `Amount delivered`, en el cual va a haber un cuadro de texto donde debemos colocar la cantidad de dinero dada por el comprador para cancelar la cuenta de la factura. Este se almacenara en la entrada de `cash_entry`.

```python
        def update_payment_fields():
            for widget in payment_frame.winfo_children():
                widget.destroy()
            if payment_method.get() == "cash":
                ttk.Label(
                    payment_frame, text="Amount delivered:"
                ).pack(side="left")
                cash_entry = ttk.Entry(payment_frame)
                cash_entry.pack(side="left")
                payment_frame.cash_entry_ = cash_entry
                payment_frame.card_entry_ = None
```

En caso de que se haya escogido tarjeta como medio de pago, se generara entonces un campo llamado `Card Number (4 last numbers)` con un cuadro de texto en el cual debemos ingresar los ultimos cuatro digitos de la tarjeta designada como metodo de pago. Este se almacenara en la entrada de `card_entry`. Finalmente, sea cual haya sido el metodo de pago elegido, se ejecutara la funcion `update_payment_fields`.

```python
            else:
                ttk.Label(
                    payment_frame, text="Card Number (4 last numbers):"
                ).pack(side="left")
                card_entry = ttk.Entry(payment_frame)               
                card_entry.pack(side="left")
                payment_frame.card_entry_ = card_entry
                payment_frame.cash_entry_ = None

        payment_method.trace_add(
            "write", lambda *args: update_payment_fields()
        )
        update_payment_fields()
```

Definimos la funcion `submit`, con la cual vamos a crear nuestra factura en formato .PDF con todos los datos diligenciados previamente. Primeramente se debe verificar que, sea cual haya sido el actor de la factura, si se escogio un actor existente, este sea un actor valido y este en el sistema.

```python
        def submit():
            try:
                if actor_mode.get() == "existent":
                    if (
                        actor_var.get() and 
                        actor_var.get() != "It's not actors available"
                    ):
                        actors_dict = (
                            self.system.customers 
                            if actor_type.get() == "customer" 
                            else self.system.suppliers
                        )
                        actor = next(
                            (
                                a for a in actors_dict.values() 
                                if a.name == actor_var.get()
                             ), None
                        )
                    else:
                        raise ValueError("You must select a valid actor.")
```

Si se escogio crear un actor nuevo, entonces se debe verificar que todos los campos hayan sido diligenciados correctamente. En caso de que falte diligenciar algun campo de estos, retornara el mensaje `Enter the new actor's information`. Si todo esta diligenciado correctamente entonces se guardara la informacion diligenciada en un objeto `customer` o `supplier` dependiendo el caso.

```python
                else:
                    actor_name = new_actor_name.get().strip()
                    actor_contact = new_actor_contact.get().strip()
                    if not actor_name or not actor_contact:
                        raise ValueError(
                            "Enter the new actor's information."
                        )
                    actor = (
                        Customer(actor_name, actor_contact) 
                        if actor_type.get() == "customer" 
                        else Supplier(actor_name, actor_contact)
                        )
```

Se crea una lista vacia llamada `manual_movements`, en donde se guardaran todos los movimientos manuales que realicemos. Para cada producto y cantidad guardada en la lista de `items`, entonces crea un objeto `Movement` con los parametros de codigo, cantidad, actor y el texto `"Manual sell"`.

```python
                manual_movements = []
                for product, qty in items:
                    manual_movements.append(
                        Movement(product, qty, actor, "Manual sell")
                    )
```

En caso de haber movimientos pendientes en la listbox de pendientes, estara la opcion de seleccionar cuales se quieren pagar, sin importar si es una, dos, todas, la primera, la ultima, o las que sean. Sin embargo, en caso de que no se hayan agregado productos para pagar, y que tampoco se hayan seleccionado movimientos pendientes o directamente no hayan movimientos pendientes, entonces el sistema retornara el mensaje `At least one movement is required for billing`.

```python
                selected_indexes = pending_listbox.curselection()
                selected_pending = [
                    pending_movements[i] for i in selected_indexes
                ]

                all_movements = manual_movements + selected_pending
                if not all_movements:
                    raise ValueError(
                        "At least one movement is required for billing."
                    )
```

Se crea una variable `total` que consta de la suma del precio total de todos los productos agregados y movimientos a pagar.

```python
                total = sum(
                    m.product._price * m.amount for m in all_movements
                )
```

Si el metodo de pago seleccionado es de `cash`, entonces se debe verificar que se haya ingresado un monto del dinero entregado, o retornara el error `"Cash entry not found"`. En caso de que si se haya ingresado, se debe verificar que el dato ingresado sea un valor flotante. Si la entrada es valida, entonces a la variable `payment` se le asigna `cash_entry` como un flotante.

```python
                if payment_method.get() == "cash":
                    cash_entry = payment_frame.cash_entry_
                    if not cash_entry:
                        raise ValueError("Cash entry not found.")
                    payment = Cash(float(cash_entry.get().strip()))
```

Si el metodo de pago seleccionado es de `card`, entonces se debe verificar que el campo se haya diligenciado, y en caso de que no, retornara el mensaje `"Card entry not found"`. Si el campo si fue diligenciado, entonces se revisa la entrada, y si esta no es un digito, o tiene una longitud diferente a 4 digitos, entonces retornara el error `"Card number must be 4 digits"`. Si la entrada es valida, entonces a la variable `payment` se le asigna la entrada de `card_entry` junto con `***` simulando el CVV de la tarjeta.

```python
                else:
                    card_entry = payment_frame.card_entry_
                    if not card_entry:
                        raise ValueError("Card entry not found.")
                    num = card_entry.get().strip()
                    if not num.isdigit() or len(num) != 4:
                        raise ValueError("Card number must be 4 digits.")
                    payment = Card(num, "***")
```

En caso de que la cantidad de pago sea insuficiente, entonces el sistema retorna el mensaje `"Insufficient payment"`.

```python
                if not payment.pay(total):
                    raise ValueError("Insufficient payment.")
```

Si se selecciono el modo de actor `new`, entonces, si se selecciono al cliente `customer`, el actor se guarda en `system.add_customer`, pero si se seleciono `supplier`, entonces el actor se guarda en `system. add_supplier`.

```python
                if actor_mode.get() == "new":
                    if actor_type.get() == "customer":
                        self.system.add_customer(actor)
                    else:
                        self.system.add_supplier(actor)
```

Cada movimiento en la lista `manual_movements` se guarda en `system.add_movement`.

```python
                for movement in manual_movements:
                    self.system.add_movement(movement)
```

El objeto `bill` se guarda en `system.create_bill` y se le asignan los atributos `actor`, `all_movements` y `payment`. En caso de que ocurra un error, se retornara el mensaje `"Failed to create bill"`.

```python
                bill = self.system.create_bill(actor, all_movements, payment)
                if bill is None:
                    raise RuntimeError("Failed to create bill")
```

Si todo el proceso de la creacion de la factura se ejecuta correctamente, entonces se exportara la factura en formato .PDF con la funcion `export_bill_pdf` con el nombre de `Bill_{bill.entity.name}.pdf`. Se mostrara el mensaje `"Success", "Bill created with ID:"` y especifica el ID de la factura. Finalmente se cierra la ventana.

```python
                self.system.export_bill_pdf(
                    bill._bill_id, f"Bill_{bill.entity.name}.pdf"
                )

                messagebox.showinfo(
                    "Success", f"Bill created with ID: {bill._bill_id}"
                )
                dialog.destroy()
```

En caso de que ocurra algun error, se genera un messagebox con el mensaje `"Error", "Couldn't create the bill"`.

```python
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Couldn't create the bill:\n{str(e)}"
                )
```

Al final de la ventana, se encuentra el boton llamado `Create bill` con el cual ejecutaremos el comando `submit`.

```python
        ttk.Button(
            main_frame, text="Create bill", command=submit
        ).pack(pady=10)
```

Definimos la función `export_movements_report` para poder exportar el reporte de movimientos en formato .PDF. Si la exportacion es exitosa, entonces se genera un messageboz con el mensaje `"Success", "Moevments report saved as 'movement_report.pdf'"`. Si hubo algun error en la exportacion, el messagebox tendra el mensaje `"Error"` y especificara el error ocurrido.

```python
    def export_movements_report(self):
        try:
            self.system.export_movements_pdf()
            messagebox.showinfo(
                "Success", "Movements report saved as 'movement_report.pdf'."
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
```

Definimos la función `export_bill` para exportar la factura en formato .PDF. Se genera una ventana emergente de tipo `simple_input_dialog` donde debemos ingresar el ID de la factura que queremos exportar. Si esta factura no se encuentra registrada en el diccionario de facturas `system.bills`, entonces sale un messagebox con el mensaje `"Error", "No bill exists with ID:"` y el ID escrito.

```python
    def export_bill(self):
        bill_id = simple_input_dialog("Enter the ID of the bill:")
        if bill_id not in self.system.bills:
            messagebox.showerror(
                "Error", f"No bill exists with ID: {bill_id}"
            )
            return
```

Si el ID se encuentra vinculado a una factura, entonces se abre el explorador de archivos donde podremos escribir con que nombre queremos llamar la factura, siempre y cuando sea en formato .PDF (que se pondra como formato por defecto), pero si no se pone nada en el nombre igual exporta la factura, y se genera un messagebox con el mensaje `"Success", "Bill exported as"` y especifica el nombre del documento. En caso de que ocurra algun error, se genera un messagebox con el mensaje `"Error", "Couldn't export the bill"`.

```python
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
            )
            if not filename:
                return
            self.system.export_bill_pdf(bill_id, filename)
            messagebox.showinfo("Success", f"Bill exported as:\n{filename}")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Couldn't export the bill:\n{str(e)}"
            )
```

Definimos la función `generate_sales_summary` para generar el resumen de ventas. Se genera una ventana emergente llamada `Sales Summary` donde hay un campo donde nos preguntan `Do you want to generate for a specific product?`. En este campo deberiamos ingresar el producto al cual queramos generarle el resumen de ventas, y en caso de que este se encuentre guardado, se mostrara el texto `"Let it blank to generate the general report"`.

```python
    def generate_sales_summary(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Sales Summary")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=12)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame, text="Do you want to generate for a specific product?"
        ).pack(padx=10, pady=5)

        product_code_var = tk.StringVar()
        ttk.Entry(
            main_frame, textvariable=product_code_var
        ).pack(padx=10, pady=5)
        ttk.Label(
            main_frame, text="(Let it blank to generate the general report)"
        ).pack(pady=5)
```

Aqui definimos la funcion `submit` que sera la encargada de enviar al sistema el codigo que ingresamos previamente para verificar si dicho producto se encuentra en la biblioteca `system.records`. En caso de que no hayan productos, se genera un messagebox con el mensaje `"Error", "There're no registered products in the system"`.

```python
        def submit():
            product_code = product_code_var.get().strip() or None
            if not self.system.records:
                messagebox.showerror(
                    "Error", "There're no registered products in the system."
                )
                return
```

El codigo del producto que ingresamos, la funcion la buscara en la biblioteca `system.movements`. En caso de que el codigo no se encuentre en la biblioteca, se generara un messagebox con el mensaje `"Error", "The product code doesn't exist"`.

```python
            if product_code:
                codes = {m.product._code for m in self.system.movements}
                if product_code not in codes:
                    messagebox.showerror(
                        "Error", 
                        f"The product code '{product_code}' doesn't exist."
                    )
                    return
```

Si el codigp ingresado si se encuentra registrado, entonces se creara el archivo llamado `Sales_summary.pdf` con el codigo del producto. Se generara un messagebox con el mensaje `"Success", "Summary generated in 'sales_summary.pdf'"` y se cerrara la ventana. En caso de que ocurra algun error, el messagebox tendra el mensaje `"Error", "Couldn't generate the summary"`. Al final de la ventana se encuentra el boton `Generate` el cual accionara la funcion `generate_sales_summary`.

```python
            try:
                self.system.export_sales_summary_pdf(
                    filename="sales_summary.pdf", product_code=product_code
                )
                messagebox.showinfo(
                    "Success", "Summary generated in 'sales_summary.pdf'"
                )
                dialog.destroy()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Couldn't generate the summary:\n{e}"
                )

        ttk.Button(main_frame, text="Generate", command=submit).pack(pady=10)
```

Definimos la función `show_restock_suggestions` para mostrar todas las sugerencias de restock que debemos hacer a nuestro inventario. Estas sugerencias las tomaremos del diccionario de sugerencias `system.restock_suggestions`. Si no hay sugerencias de restock de inventario registradas en dicho diccionario, entonces se generara un messagebox con el mensaje `"Info", "There are no restock suggestions"`.

```python
    def show_restock_suggestions(self):
        suggestions = self.system.restock_suggestions()

        if not suggestions:
            messagebox.showinfo("Info", "There are no restock suggestions.")
            return
```

En caso de que si hayan sugerencias reportadas, se genera una nueva ventana emergente llamada `Restock Suggestions`, en donde vamos a encontrar un frame llamado `Low-Stock Products` y definiremos el objeto `cols` con los valores `Code`, `Product`, `Current` y `Minimum`. Con estos valores de `cols` generaremos un Treeview donde cada columna toma como nombre estos valores.

```python
        dialog = tk.Toplevel(self.root)
        dialog.title("Restock Suggestions")
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame, text="Low-Stock Products"
        ).grid(row=0, column=0, columnspan=2, pady=(0,15))

        cols = ("Code", "Product", "Current", "Minimum")
        tree = ttk.Treeview(
            main_frame, columns=cols, show="headings", style="Treeview"
        )
```

A cada columna le asignaremos su respectivo titulo, y al Treeview le daremos una Scrollbar, esto para hacer la interfaz mas amigable con el usuario.

```python
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center")
        tree.grid(row=1, column=0, sticky="nsew")

        sb = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=sb.set)
        sb.grid(row=1, column=1, sticky="ns")

        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
```

De cada item contenido en `suggestions`, traeremos sus valores de codigo, nombre, stock actual, y minimo requerido, y estos valores los colocaremos en el Treeview en su respectivo orden para crear una lista de sugerencias con todas las contenidas en su diccionario.

```python
        for item in suggestions:
            tree.insert("", "end", values=(
                item["Code"],
                item["Name"],
                item["Current Stock"],
                item["Minimum Required"]
            ))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
```

Definimos la funcion `export_pfd` para generar este documento con todas las sugerencias de restock, y exportarlo en formato .PDF. Se abrira el explorador donde le podemos colocar nombre a nuestro archivo, y se guardara en formato .PDF por defecto. Si el usuario no selecciono una ruta de guardado, se generea un messagebox con el mensaje `"Success", "PDF generated in"` y especifica la ruta seleccionada por defecto.

```python
        def export_pdf():
            path = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
            )
            if not path:
                return
            ok = self.system.export_critical_stock_pdf(path)
            if ok:
                messagebox.showinfo("Success", f"PDF generated in:\n{path}")
```

Si no hay sugerencias de restock entonces el messagebox tendra el mensaje `"Info", "There're not critical stocks to generate a PDF"`. Al final se encuentra el boton llamado `Export PDF` con el cual se inicializa el comando `export_pdf`, y otro boton llamado `Close` para poder cerrar la ventana.

```python
            else:
                messagebox.showinfo(
                    "Info", "There're not critical stocks to generate a PDF."
                )

        ttk.Button(
            button_frame, text="Export PDF", command=export_pdf
        ).grid(row=0, column=0, padx=5)
        ttk.Button(
            button_frame, text="Close", command=dialog.destroy
        ).grid(row=0, column=1, padx=5)
```

Definimos la función `simple_input_dialog` como una ventana emergente llamada `Input` en la cual vamos a poder ingresar cualquier value que se requiera dependiendo de la seccion de donde se ejecute el comando.

```python
def simple_input_dialog(prompt):
    dialog = tk.Toplevel()
    dialog.title("Input")
    dialog.resizable(False, False)
    dialog.grab_set()

    dialog.update_idletasks()
    width = 300
    height = 130
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")

    frame = ttk.Frame(dialog, padding=15)
    frame.pack(fill="both", expand=True)

    label = ttk.Label(frame, text=prompt)
    label.pack(padx=10, pady=(0, 10))
    entry = ttk.Entry(frame, width=30)
    entry.pack()
    entry.focus_set()
```

Definimos la funcion `submit` con la cual, el valor que hayamos colocado en esta pestaña lo mandaremos a la ventana de donde es solicitada, y cerrara la ventana. En la ventana hay un boton llamado `OK`, el cual tiene el comando `submit`.

```python
    def submit():
        dialog.result = entry.get()
        dialog.destroy()

    button = ttk.Button(frame, text="OK", command=submit)
    button.pack(pady=(10, 5))

    dialog.bind("<Return>", lambda event: submit())
    dialog.wait_window()
    return getattr(dialog, 'result', None)
```

---------









