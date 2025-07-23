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


En la clase `Product`, a través del método `__init__`, vamos a definir los productos que harán parte de nuestro sistema de inventario. Cada producto tiene cinco atributos principales: `name`, `category`, `code`, `price` y `state`. El atributo name representa el nombre comercial del producto, mientras que `category` nos permite clasificarlo dentro de una categoría general (como por ejemplo: "Vegetables" o "Grains"). El campo `code`, que está protegido mediante el uso del guion bajo (`_code`), corresponde al identificador interno del producto, que permite distinguirlo del resto en el sistema. A su vez, `price` (también con acceso protegido como `_price`) indica el valor monetario del producto, y `state` es un objeto que describe su estado actual. Este último puede ser `None` si no se ha definido un estado al momento de crear el producto.


```python
class Product:
    def __init__(self, name, category, code, price, state):
        self.name = name
        self.category = category
        self._code = code
        self._price = price
        self._state = state
```

Con el método `to_dict` vamos a convertir cada instancia de `Product` en un diccionario de Python, útil para tareas como el almacenamiento en bases de datos con los Json. El diccionario incluye claves como `"name"`, `"category"`, `"code"`, `"price"` y `"state"`, y sus respectivos valores corresponden a los atributos del objeto. En particular, si el atributo `_state` existe, también será convertido a un diccionario mediante su propio método `to_dict`; de lo contrario, se registrará como `None`.

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
Esta estructura nos permite mantener toda la información del producto organizada y fácilmente accesible para su procesamiento dentro del sistema de inventario.


#### State

La clase `State` representa el estado en el que se encuentra un producto del inventario. Cada instancia debe contener al menos uno de los dos atributos: una condición (`condition`) o una fecha de expiración (`expiration_date`). Aunque ambos parámetros son opcionales en la firma del constructor, la lógica del sistema asume que como mínimo uno debe estar presente para que el estado tenga sentido.

```python
class State:
    def __init__(self, condition = None, expiration_date = None):
        self._condition = condition
        self._expiration_date = expiration_date
```

El atributo `_condition` es una cadena que puede representar, por ejemplo, que el producto está "Fresco", por ejemplo(este se usa para productos como `Fruits` o `Vegetables`). Por su parte, `_expiration_date` debe recibirse como una tupla de tres valores (`YYYY`, `MM`, `DD`), y representa la fecha en la que el producto deja de ser válido o útil (este se usa para productos empacados con su fecha de vencimiento especifica). Aunque ninguno de los dos campos es obligatorio por separado, el sistema espera que al menos uno esté definido.

Uno de los métodos centrales es `is_expired`, el cual permite verificar si la fecha de expiración del producto ya pasó. Si se ha definido `_expiration_date`, se convierte en un objeto `datetime.date` y se compara con la fecha actual. Si el producto no tiene fecha de expiración, el método simplemente retorna `False`.

```python
    def is_expired(self):
        if self._expiration_date:
            today = datetime.date.today()
            expiration = datetime.date(*self._expiration_date)
            return today > expiration
        return False
```
El método `to_dict` convierte el estado del producto en un diccionario. Si el estado tiene una condición, se incluirá bajo la clave `"condition"`; si tiene una fecha de expiración, se incluirá como `"expiration_date"`. Si ambos están presentes, ambos se reflejan en el diccionario.

```python
    def to_dict(self):
        state_dict = {}
        if self._condition is not None:
            state_dict["condition"] = self._condition
        if self._expiration_date is not None:
            state_dict["expiration_date"] = self._expiration_date
        return state_dict
```
Además, la clase implementa el método especial `__str__`, que genera una representación legible del estado del producto. Si existe una condición válida, se mostrará como `"Condition: <condición>"`. Si hay fecha de expiración, se mostrará en el formato `"Expires: YYYY-MM-DD"`. Cuando ambos atributos existen, se concatenan separados por coma; si no hay ninguno (aunque esto no debería suceder según la lógica del sistema), se devuelve la cadena `"Unknown"`.

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
En resumen, la clase `State` permite describir el estado físico o temporal de un producto, garantizando que al menos haya un criterio para determinar si ese producto está en condiciones de uso, vencido o necesita revisión. Esta clase puede integrarse fácilmente con otras partes del sistema mediante sus métodos `to_dict` y `__str__`.


-----------

<h3 align="center"> Inventory_Management </h3>

#### Inventory Record:

En la clase `InventoryRecord`, por medio del método `__init__` se definen los atributos que va a tener el registro de nuestro inventario, como serían: `product`, `stock` y `location`. Estos van a actuar como objetos.

```python
class InventoryRecord:
    def __init__(self, product, stock, location):
        self.product = product
        self.stock = stock
        self.location = location
```

Referenciamos los atributos propios de nuestra clase `InventoryRecord` por medio de nuestro constructor `self` con los nombres de `product`, `stock` y `location`.

```python
    def to_dict(self):
        return {
            "product": self.product.to_dict(),
            "stock": self.stock.to_dict(),
            "location": self.location.to_dict()
        }
```

Convertimos los atributos de nuestra clase `InventoryRecord` en un diccionario con las claves: `product`, `stock` y `location`.

#### Location:

Creamos la clase `Location` a la cual le vamos a asignar unos atributos protegidos que están fuera del constructor y son compartidos entre todas las instancias de la clase. Estos son `_category_aisles` que es la categoría de cada uno de los pasillos y es un diccionario vacío; `_next_aisle_number` que dicta cual será el siguiente pasillo pasando de uno en uno; `_shelf_counter_by_category` que cuenta cuantos estantes ya han sido asignados por categoría (también es un diccionario vacío); `_product_shelving = {}` que es un diccionario de las estanterias de cada producto.

```python
class Location:
    _category_aisles = {}
    _next_aisle_number = 1
    _shelf_counter_by_category = {}
    _product_shelving = {}
```

Definimos los atributos de nuestra clase `Location`, los cuales son `aisle` (pasillos) y `shelf` (estantes).

```python
    def __init__(self, aisle, shelf):
        self.aisle = aisle
        self.shelf = shelf
```

Con el decorador `@classmethod` indicamos que el metodo trabaja con la clase completa. Definimos el metodo `sync_from_inventory` para que, por cada registro en el diccionario de registros, se le asigne un pasillo y estante y se tomen las variables `category`, `code`, `aisle` y `shelf`.

```python
    @classmethod
    def sync_from_inventory(cls, records):
        for record in records:
            category = record.product.category
            code = record.product._code
            aisle = int(record.location.aisle)
            shelf = int(record.location.shelf)
```

Si la categoria no se encuentra asignada a un pasillo especifico, este metodo le asignara uno disponible.

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

Con el decorador `@classmethod` indicamos que el metodo trabaja con la clase completa y no solo con objetos individuales. Definimos el método `assign_location`. Si la instancia de categoría `category` no tiene un pasillo asignado, se le asignara uno disponible, de forma que si hay un pasillo ocupado, se revisara el siguiente hasta que se encuentre uno disponible. Se tomaran las variables `aisle` y `key`.

```python
    @classmethod
    def assign_location(cls, category, code):
        if category not in cls._category_aisles:
            cls._category_aisles[category] = cls._next_aisle_number
            cls._next_aisle_number += 1
        aisle = cls._category_aisles[category]
        key = (category, code)
```

Si la `key` esta en un pasillo, a la variable `shelf` se le asignará esta. En caso de que no, se le asignara un pasillo diponible comenzando desde 0 y verificando uno por uno a ver cual esta disponible.

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

Por medio del método `to_dict` vamos a convertir la información de la ubicación del producto a un diccionario con las claves `aisle` y `shelf`.

```python
    def to_dict(self):
        return {
            "aisle": self.aisle,
            "shelf": self.shelf
        }
```

#### Stock:

Del modulo `Inventory_System.Transactions.movements` importamos la clase `Movement`.

```python
from Inventory_System.Transactions.movements import Movement
```

Creamos la clase `Stock` con atributos como `actual_stock`, `mínimum_stock`, `máximum_stock` y `_record` que es una lista vacia.

```python
    def __init__(self, actual_stock, minimum_stock, maximum_stock):
        self._actual_stock = actual_stock
        self.minimum_stock = minimum_stock
        self.maximum_stock = maximum_stock
        self._record = []
```

Se define el método `get_actual_stock` el cual, en caso de querer consultar el stock actual, nos lo va a retornar.

```python
    def get_actual_stock(self):
        return self._actual_stock
```

Se define el método `is_valid_update` con un atributo `delta` que representa el cambio de stock. El método revisa que antes de que se modifique el stock, el cambio no deje el stock ni por debajo del mínimo, ni por encima del máximo permitido.

```python
    def is_valid_update(self, delta):
        new_stock = self._actual_stock + delta
        return 0 <= new_stock <= self.maximum_stock
```

El método `update_stock` se define para actualizar el stock de un producto. Por medio de este método, si la actualización del stock no es válida, retornara el mensaje `”Cannot update stock”`. En caso de que si sea válida, se sumara el movimiento `delta` al stock actual ya sea entrada o salida. Si se paso un movimiento, se guarda en el diccionario de registros, si no, retorna el mensaje `”Only Movement instances are allowed to update stock”`.

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

Definimos el método `update_stock_limits` con las instancias `new_min` y `new_max` para poder actualizar el mínimo y máximo de stock de algún producto. En caso de que se quiera actualizar el mínimo o máximo stock a un valor menor a 0, retornara el mensaje de error `”Stock limits cannot be negative”`. En caso de que se quiera actualizar el mínimo stock, y que este sea superior al máximo stock, retornara el mensaje de error `”Minimum stock cannot exceed máximum stock”`. En caso de que el cambio sea correcto, se actualizará.

```python
    def update_stock_limits(self, new_min, new_max):
        if new_min < 0 or new_max < 0:
            raise ValueError("Stock limits cannot be negative.")
        if new_min > new_max:
            raise ValueError("Minimum stock cannot exceed maximum stock.")
        self.minimum_stock = new_min
        self.maximum_stock = new_max
```

El método `to_dict` retorna el stock actual, el stock mínimo y el stock máximo en diccionario con las claves `actual_stock`, `mínimum_stock` y `máximum_stock`.

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

En la clase `Inventory` definimos dos atributos donde almacenaremos datos, que se crean directamente desde el objeto sin necesidad de recibirlos como parámetro. Estos son: `self.records` que es un diccionario vacío, y `self.movements` que es una lista vacía.

```python
class Inventory:
    def __init__(self):
        self.records = {}
        self.movements = []
```

Definimos la función `add_record`, la cual nos servira para añadir un registro al diccionario de registros con el codigo del producto, esto en caso de que este no se encuentre en el diccionario. SI el producto ya se encuentra en el diccionario, retorna un mensaje de error `"This product already exists in the inventory"`.

```python
    def add_record(self, record):
        code = record.product._code
        if code not in self.records:
            self.records[code] = record
        else:
            print("This product already exists in the inventory.")
```

Se definió la función `remove_record` para, como lo dice su nombre, poder remover el registro de código de un producto por medio de la instrucción `del`. La función va a buscar el código de la biblioteca de registros. Si se encuentra el código, se procede con la función correctamente y se elimina el registro de la biblioteca. Si el código no se encuentra, el sistema arroja el mensaje “*No record found with this code*”.

```python
    def remove_record(self, code):
        if code in self.records:
            del self.records[code]
        else:
            print("No record found with this code.")
```

Se define el metodo `update_stock_limits`, con el que vamos a actualizar los limites minimos y maximos de stock de un producto permitidos. En caso de que el codigo de producto no se encuentre en el diccionario de registros, retornara el mensaje de error `"Product not found in inventory records"`.

```python
    def update_stock_limits(self, product_code:str, new_min:int, new_max:int):
        if product_code not in self.records:
            raise ValueError("Product not found in inventory records.") 
        self.records[product_code].stock.update_stock_limits(new_min, new_max)
```

Cada cambio de cantidad (definido como `movement`), ya sea ingreso o salida de productos, se almacenará en la lista de movimientos con el comando `self.movements.append(movement)`. Si la actualizacion de stock aplica, entonces esta se guardara en el diccionario de registros con por codigo de producto (`product_code`). `delta` se define como el cambio de cantidad de inventario de los productos, ya sea positivo o negativo. Posteriormente se actualiza el stock mediante el comando `self.records[product_code].stock.update_stock(delta, movement)`, que toma el código del producto y el método `update_stock()` de `stock` es el que se encarga de actualizar el inventario del producto. 

```python
    def add_movement(self, movement, apply_stock: bool = True):
        self.movements.append(movement)
        if apply_stock:
            product_code = movement.product._code
            delta = movement.get_delta()
            self.records[product_code].stock.update_stock(delta, movement)
```

En caso de que se quiera consultar cada movimiento, se definió la función `get_movements_by_code`, que permite hacer la consulta de todos los movimientos en forma de lista de un producto en especifico por medio de su código.

```python
    def get_movements_by_code(self, code):
        return [
            movement for movement in self.movements if 
                movement.product.code == code
        ]
```

El metodo `get_critical_records` lo usamos para que, por cada registro en el diccionario de registros, nos retorne todos los registros de productos cuyo stock actual este por debajo del minimo permitido.

```python
    def get_critical_records(self):
        return [
            r for r in self.records.values()
            if r.stock.get_actual_stock() < r.stock.minimum_stock
        ]
```

El método `restock_suggestions` sugiere que productos necesitan ser reabastecidos según el mínimo establecido, es decir que tienen stock por debajo de este. Este toma los productos de la lista del metodo `get_critical_records` y nos retorna los valores de estos productos con las claves `Name`, `Code`, `Current Stock` y `Minimum Required`.

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

En la clase `Customer`, por medio del metodo `__init__` vamos a definir a nuestro cliente, con atributos principales como `name`, `number_id` y `customer_id`.

```python
import uuid

class Customer:
    def __init__(self, name, number_id, customer_id=None):
        self.name = name
        self.number_id = number_id
        self._id = customer_id if customer_id else str(uuid.uuid4())
```

Mediante el constructor `self` referenciamos los atributos que va a tener nuestra clase `Customer`, los cuales son `name`, `number_id` y un `customer_id` con el cual vamos a usar la librería `uuid` para generarle a cada cliente un identificador único universal (UUID), para que por seguridad estos no se repitan, ya que es extremadamente improbable que esto pase. Con la versión de UUID `uuid4` vamos a obtener un identificador completamente aleatorio, lo que aumenta la seguridad exponencialmente; sin embargo, en caso de requerirse, también se puede escribir el identificador de un cliente de forma manual. 

```python
    def to_dict(self):
        return {
            "name": self.name,
            "number_id": self.number_id,
            "_id": self._id
        }
```
 
Con el método `to_dict` vamos a convertir los objetos de la clase `Customer` en un diccionario de Python con las claves: `name`, `number_id` y `_id`.

#### Supplier:

En la clase `Supplier`, por medio del metodo `__init__` tambien vamos a definir a nuestro proveedor, con atributos principales como `name`, `contact_number` y `supplier_id`.

```python
import uuid

class Supplier:
    def __init__(self, name, contact_number, supplier_id=None):
        self.name = name
        self.contact_number = contact_number
        self._id = supplier_id if supplier_id else str(uuid.uuid4())
```

Por medio del constructor `self` vamos a referenciar también los atributos de nuestra clase `Supplier`, los cuales serian similares a los de la clase anterior, pero no los mismos. En este caso los atributos serian `name`, `contact_number` (cambia en relación con la clase `Customer`) y `supplier_id`, que al igual que con la clase anterior, vamos a randomizar por medio de la versión de UUID `uuid4`.

```python
    def to_dict(self):
        return {
            "name": self.name,
            "contact_number": self.contact_number,
            "_id": self._id
        }
```

Al igual que con la clase anterior, vamos a convertir los objetos de nuestra clase `Supplier` en un diccionario con las claves: `name`, `contact_number` y `_id`.

-----------

<h3 align="center"> Transactions </h3>

#### Movements:

Importamos la biblioteca `datetime`, y de el modulo `Inventory_System.People`, importamos `Customer` y `Supplier`.

```python
from datetime import datetime
from Inventory_System.People.customer import Customer
from Inventory_System.People.supplier import Supplier
```

La clase `Movement` representa un registro individual de movimiento de inventario. Cada movimiento está relacionado con un producto, una cantidad (`amount`), una razón o motivo del movimiento, y un actor (cliente o proveedor) que lo genera. También se registra la fecha y se determina si el movimiento es de entrada o salida.

El constructor `__init__` es un método inicializa un nuevo movimiento con la información proporcionada: el producto involucrado, la cantidad de unidades, el actor (cliente o proveedor) que lo realiza, y la razón del movimiento.

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
-Se guarda la referencia del producto y la cantidad (`amount`) directamente.

-Se utiliza `datetime.now()` para capturar la fecha del movimiento al momento de su creación.

-Se valida que el actor sea una instancia de `Customer` o `Supplier`; de lo contrario, lanza un error tipo `TypeError`.

-Se almacena el identificador del actor (`_actor_id`) y se clasifica si es un cliente o un proveedor mediante `actor_type`.

-Automáticamente, el tipo de movimiento se establece como `"out"` si lo realiza un cliente (salida del inventario), o como `"in"` si lo realiza un proveedor (entrada al inventario).

-Por último, se guarda la razón del movimiento.

El metodo `get_delta` calcula el cambio que representa este movimiento sobre el inventario del producto.

```python
    def get_delta(self):
        return self.amount if self.type == "in" else -self.amount
```
-Si el movimiento es de entrada (`"in"`), devuelve la cantidad en positivo.

-Si el movimiento es de salida (`"out"`), devuelve la cantidad como negativa.

-Este resultado puede utilizarse directamente para actualizar el inventario del producto.

El metodo `to_dict` convierte el movimiento en un diccionario de Python, ideal para serialización, almacenamiento o impresión estructurada.

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
Devuelve la información clave del movimiento, como el nombre y código del producto, la cantidad, el tipo de movimiento (`in` o `out`), la fecha formateada, el nombre del actor y su ID, y la razón registrada.

#### Payment:
En la clase `Payment`, vamos a definir una clase base abstracta para todos los métodos de pago. Es decir, esta clase no se va a usar directamente para hacer pagos, sino que sirve como plantilla para las clases hijas como `Card` y `Cash`. En ella definimos dos métodos (`pay` y `to_dict`) que deben ser implementados por las subclases.

```python
class Payment:
    def __init__(self):
        pass

    def pay(self, amount):
        raise NotImplementedError("Subclasses must implement the pay() method.")

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement the to_dict() method.")
```

La clase `Card` hereda de `Payment`, y representa un método de pago con tarjeta. En su constructor (`__init__`) recibimos el número de tarjeta y el código CVV. Usamos `super()` para llamar al constructor de la clase base.

```python
class Card(Payment):
    def __init__(self, number, cvv):
        super().__init__()
        self._number = number
        self._cvv = cvv
```
El método `pay` en esta clase simula la acción de pagar con tarjeta. Imprime un mensaje en consola que indica cuánto se va a pagar y muestra los últimos 4 dígitos del número de la tarjeta.

```python
    def pay(self, amount):
        print(f"Paying {amount} with card ending in {self._number[-4:]}")
        return True
```

El método `to_dict` convierte los datos de la tarjeta en un diccionario, ocultando el número completo por motivos de seguridad. Solo muestra los últimos 4 dígitos.

```python
    def to_dict(self):
        return {
            "method": "Card",
            "card_number": f"**** **** **** {self._number[-4:]}"
        }
```

Finalmente, con el método `__str__`, devolvemos una representación en texto legible del objeto `Card`, también mostrando solo los últimos dígitos del número.

```python
    def __str__(self):
        return f"Card - **** **** **** {self._number[-4:]}"
```

La clase `Cash` también hereda de `Payment`, pero representa pagos en efectivo. En su constructor, se guarda el valor entregado por el cliente.

```python
class Cash(Payment):
    def __init__(self, cash_given):
        super().__init__()
        self.cash_given = cash_given
```

El método `pay` verifica si el efectivo entregado es suficiente para cubrir el valor del pago. Si es suficiente, calcula el cambio y lo imprime; si no lo es, informa cuánto falta.

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

El método `to_dict` convierte los datos de pago en efectivo en un diccionario que guarda el método y el valor entregado.

```python
    def to_dict(self):
        return {
            "method": "Cash",
            "cash_given": self.cash_given
        }
```

Finalmente, `__str__` devuelve una representación legible del objeto `Cash`, indicando cuánto dinero entregó el cliente.

```python
    def __str__(self):
        return f"Cash - Given: ${self.cash_given:.2f}"
```

#### Bills:
Este módulo permite gestionar facturas de compras o ventas, asociadas a una entidad (ya sea un cliente o un proveedor), con una lista de productos, sus cantidades, precios y el método de pago correspondiente.

La clase `BillItem` representa un único ítem dentro de una factura. Contiene tres atributos esenciales: el `producto`, la `cantidad` adquirida, y el `precio` unitario de dicho producto.

```python
class BillItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
```

Con el método `get_total_price`, calculamos el precio total del ítem multiplicando la cantidad por el precio unitario.

```python
    def get_total_price(self):
        return self.quantity * self.price
```

El método `to_dict` permite convertir el ítem a un diccionario de Python, útil para serialización o almacenamiento. Incluye el nombre y código del producto, la cantidad, el precio unitario y el total.

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

La clase `Bill` representa una factura completa. Esta incluye una entidad (puede ser un cliente o un proveedor), la fecha de emisión, un identificador único, el método de pago, y una lista de ítems (`BillItem`) que componen la factura.

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
En este constructor, se genera automáticamente un ID único para la factura usando `uuid4`, y se registra la fecha actual usando `datetime.now()`. Se identifica el tipo de entidad (`Customer` o `Supplier`) verificando la clase del objeto recibido. También se inicializa la lista vacía de ítems que luego se agregarán a la factura.

Con el método `add_item`, se agregan productos a la factura. Se crea un nuevo objeto `BillItem` con el producto, cantidad y precio, y luego se añade a la lista de ítems.

```python
    def add_item(self, product, quantity, price):
        item = BillItem(product, quantity, price)
        self.items.append(item)
```

El método `calculate_total` suma el total de todos los ítems que han sido agregados a la factura, usando la función `get_total_price` definida en cada `BillItem`.

```python
    def calculate_total(self):
        return sum(item.get_total_price() for item in self.items)
```

Finalmente, `to_dict` convierte toda la información de la factura en un diccionario estructurado. Esto incluye el ID, la fecha en formato año-mes-día, el nombre de la entidad, su tipo, el método de pago (convertido a diccionario si está presente), la lista de ítems (también como diccionarios), y el total general.

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

La clase `Extracts` encapsula todas las operaciones relacionadas con exportar, importar y reconstruir datos del sistema de inventario.


*Es importante aclarar que, al principio de cada metodo, se utiliza el decorador `@staticmethod` en cada uno de los métodos de la clase `Extracts` porque estos métodos no necesitan acceder ni modificar ningún atributo o estado interno de una instancia específica de la clase. Es decir, su comportamiento depende exclusivamente de los datos que reciben como argumentos, no de propiedades internas de `self`. Usar `@staticmethod` en este contexto permite organizar funcionalmente utilidades de exportación e importación dentro de una misma clase, sin necesidad de crear instancias de la misma, lo cual es más eficiente y claro desde el punto de vista del diseño del software.*

<h4 align="left"> Consultas: obtener datos desde el sistema como listas de diccionarios: </h4>

```python
@staticmethod
def get_movements(system):
    return [movement.to_dict() for movement in system.movements]
```

Este metodo recorre todos los movimientos (`system.movements`) y llama a `to_dict()` en cada uno, convirtiéndolos en diccionarios para facilitar su exportación.

```python
@staticmethod
def get_bills(system):
    return [bill.to_dict() for bill in system.bills.values()]
```
Este metodo extrae todas las facturas del sistema (system.bills es un diccionario), las convierte a diccionario con to_dict() y retorna una lista con todas ellas.

```python
@staticmethod
def get_records(system):
    return [record.to_dict() for record in system.records.values()]
```
Este metodo convierte todos los registros de inventario (que contienen productos y stock) a formato de diccionario.

```python
@staticmethod
def get_customers(system):
    return [customer.to_dict() for customer in system.customers.values()]
```
Este metodo devuelve todos los clientes del sistema como una lista de diccionarios, útil para guardarlos o reconstruirlos luego.

```python
@staticmethod
def get_suppliers(system):
    return [supplier.to_dict() for supplier in system.suppliers.values()]
```
Este metodo es similar al anterior, pero para proveedores.

#### Exportación genérica de datos a archivos `.json` 

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
Este metodo guarda cualquier `data` (lista de diccionarios) en un archivo `.json`.

Usa indentación para hacerlo legible.

`ensure_ascii=False` permite guardar caracteres especiales (como acentos).

Captura errores de escritura y lanza una excepción explicativa.

<h4 align="left"> Exportaciones específicas por tipo de objeto </h4>

Cada uno de estos métodos usa los anteriores (`get_...`) y el exportador general:

```python
@staticmethod
def export_movements(system, filename="movements.json"):
    Extracts.export_to_json(Extracts.get_movements(system), filename)
```
Este metodo exporta todos los movimientos del sistema a `movements.json`.

```python
@staticmethod
def export_bills(system, filename="bills.json"):
    Extracts.export_to_json(Extracts.get_bills(system), filename)
```
Este metodo exporta todas las facturas a bills.json.

<h4 align="left"> Exportación completa del sistema </h4>

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

Este metodo crea un diccionario con todos los datos clave del sistema, lo exporta en un solo archivo. Este archivo se puede usar como backup general o para cargar todo el sistema en otro momento.

<h4 align="left"> Importación de productos desde archivo JSON </h4>

```python
@staticmethod
def import_all_products(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return [Extracts.dict_to_product(d) for d in data]
```
Este metodo abre el archivo `filename`, luego carga los datos como una lista de diccionarios (`data`) y por cada diccionario llama al metodo `dict_to_product` para convertirlo en un objeto `Product`

<h4 align="left"> Reconstrucción de productos </h4>

```python
@staticmethod
def dict_to_product(data):
    name = data["name"]
    category = data["category"]
    code = data["code"]
    price = data["price"]
    state_data = data["state"]
```

Este bloque extrae los campos esenciales del diccionario `data`, para luego determinar el tipo de estado:

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
Lo que hace este metodo es que si el estado es un diccionario con `"expiration_date"`, lo convierte a una tupla y crea un `State`. Si tiene `"condition"`, crea un `State` con esa condición, y si el tipo de dato no es compatible lanza errores de tipo `ValueError`, para finalmente:

```python
return Product(name, category, code, price, state)
```
Retorna un objeto `Product` completo y listo para usarse.

<h4 align="left"> Conversión de entidades desde diccionarios </h4>

```python
@staticmethod
def dict_to_customer(data):
    return Customer(data["name"], data["number_id"], data["_id"])
```
Este metodo reconstruye el objeto `Customer` desde un diccionario para poder usarlo en la carga de backups
```python
@staticmethod
def dict_to_supplier(data):
    return Supplier(data["name"], data["contact_number"], data["_id"])
```
Este metodo hace lo mismo, pero esta vez con  el objeto `Supplier`

<h4 align="left"> Reconstrucción del stock (cantidad, mínimos, historial) </h4>

```python
@staticmethod
def dict_to_stock(data, system):
    actual = data["actual_stock"]
    min_stock = data["minimum_stock"]
    max_stock = data["maximum_stock"]
    stock = Stock(actual, min_stock, max_stock)
```
Este metodo crea el objeto `Stock` con sus parametros de minimo y maximo, luego reconstruye el historial.

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
Lo que hace este metodo es que, si existe un historial de movimientos (`record`) lo reconstruye, evitando movimientos duplicados al usar un set (`seen`) de claves unicas.

<h4 align="left"> Conversión de movimientos </h4>

```python
@staticmethod
def dict_to_movement(data, system):
    product_code = data["Code"]
    product = system.records[product_code].product
    amount = data["Quantity"]
    actor_id = data["Actor_ID"]
    reason = data["Reason"]
```

Este metodo recupera los campos en movimiento. Luego:

```python
if data["Type"] == "in":
    actor = system.suppliers.get(actor_id)
else:
    actor = system.customers.get(actor_id)

if actor is None:
    raise ValueError(f"Actor with ID {actor_id} not found in system")

return Movement(product, amount, actor, reason)
```
Este metodo determina si el actor es un proveedor o cliente según el tipo de movimiento. Crea un `Movement` con los datos correspondientes.

<h4 align="left"> Reconstrucción de facturas </h4>

```python
@staticmethod
def dict_to_bill(data, system):
    bill_id = data["bill_id"]
    date = data["date"]
    entity_type = data["entity_type"]
    entity_id = data.get("entity_id")
    payment_data = data["payment_method"]
```
Este metodo extrae los datos basicos de la factura. Luego:

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
Este metodo crea el objeto entidad y el método de pago adecuado. Luego se crea la factura y configura su ID y fecha:

```python
bill = Bill(entity, payment)
bill._bill_id = bill_id
bill.date = datetime.strptime(date, "%Y-%m-%d")
```
Ya por ultimo, se agregan los productos facturados:

```python
for item_data in data["items"]:
    product_code = item_data["product"]["_code"]
    product = system.records[product_code].product
    quantity = item_data["quantity"]
    price = item_data["price"]
    bill.add_item(product, quantity, price)
```

#### Carga total del sistema desde un archivo `.json`

```python
@staticmethod
def load_full_backup(path, system):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
```
Aqui se abre el archivo JSON que contiene todo el respaldo del sistema. Ahora seguimos con los metodos despues de la carga del archivo JSON

<h4 align="left"> Apertura del archivo y carga de datos </h4>

```python
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
```
Este primer bloque abre el archivo JSON que contiene el respaldo completo del sistema, utilizando la ruta proporcionada en el argumento `path`. El contenido del archivo se carga en memoria mediante `json.load(f)` y se almacena en la variable `data` como un diccionario de Python. Este diccionario contendrá claves como `"customers"`, `"suppliers"`, `"records"`, `"movements"` y `"bills"` que serán utilizadas para reconstruir los componentes del sistema.

<h4 align="left"> Carga de clientes </h4>

```python
for customer in data["customers"]:
    system.add_customer(Extracts.dict_to_customer(customer))
```
Luego, se procede a reconstruir los clientes. Para ello, se recorre cada elemento dentro de la lista `data["customers"]`, que representa los datos serializados de los clientes. Cada entrada se transforma en un objeto `Customer` usando el método auxiliar `dict_to_customer`, y luego se añade al sistema mediante `system.add_customer()`. Esto permite recuperar todos los clientes registrados antes de la exportación.

<h4 align="left"> Carga de proveedores </h4>

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
Para los proveedores, se realiza un paso adicional: antes de agregar un nuevo proveedor al sistema, se verifica si ya existe alguno con el mismo nombre y número de contacto. Si no se encuentra un proveedor duplicado, entonces se reconstruye el objeto `Supplier` a partir del diccionario usando `dict_to_supplier` y se agrega al sistema. Esto evita que se creen múltiples entradas para el mismo proveedor durante una restauración.

<h4 align="left"> Carga de registros de inventario </h4>

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
En este bloque se restauran todos los registros de inventario. Si el producto ya existe en el sistema (verificado por su código), entonces se compara su historial de movimientos. El objetivo es evitar duplicar movimientos ya registrados, para lo cual se genera una clave única para cada movimiento (producto, cantidad, actor y fecha). Si algún movimiento nuevo no está en los ya existentes, se añade al historial. Si el producto no existía previamente en el sistema, se reconstruye el registro completo con `dict_to_inventory_record` y se agrega al sistema como un nuevo elemento.

<h4 align="left"> Sincronización de ubicaciones </h4>

```python
Location.sync_from_inventory(system.records.values())
```
Una vez cargados todos los registros de inventario, se sincronizan las ubicaciones físicas de los productos. El método `sync_from_inventory` asegura que cada producto esté correctamente asignado a su estantería y pasillo dentro del sistema. Esta sincronización es importante porque la ubicación puede ser necesaria para la gestión física del inventario en el mundo real.

<h4 align="left"> Carga de movimientos </h4>

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
Aquí se restaura el historial de movimientos de productos, tanto entradas como salidas. Primero se transforma cada entrada JSON a un objeto `Movement` y se agrega al sistema. Luego, se asocia ese movimiento al historial de stock correspondiente, verificando que no esté ya registrado para evitar duplicados. Este paso garantiza que el historial completo de operaciones esté disponible para futuras consultas o auditorías, sin interferir en el stock actual (por eso `apply_stock=False`).

<h4 align="left"> Carga de facturas </h4>

```python
for bill_data in data.get("bills", []):
    bill = Extracts.dict_to_bill(bill_data, system)
    system.bills[bill._bill_id] = bill
```
Este bloque se encarga de restaurar todas las facturas del sistema. Cada factura en formato JSON se convierte en un objeto `Bill` utilizando `dict_to_bill`, que reconstruye tanto la entidad (cliente o proveedor) como el método de pago, los ítems comprados o vendidos, y la fecha. Luego, la factura se añade al sistema mediante su identificador único `_bill_id`, asegurando que las transacciones económicas queden registradas con precisión.

<h4 align="left"> Asociación entre movimientos y facturas </h4>

```python
for m in system.movements:
    for item in bill.items:
        if (m.product._code == item.product._code
            and m.amount == item.quantity
            and m.actor._id == bill.entity._id):
            m._bill_id = bill._bill_id
            break

```
Finalmente, se establece la relación entre los movimientos de inventario y las facturas a las que pertenecen. Para cada movimiento, se compara su producto, cantidad y actor con los ítems dentro de cada factura. Si se encuentra una coincidencia, se le asigna al movimiento el ID de la factura correspondiente. Este paso permite, por ejemplo, que un movimiento de salida pueda ser rastreado hasta una venta específica, lo cual es esencial para trazabilidad y control administrativo.


<h3 align="left"> generatePDF </h3>

Primero se definen las clases con sus metodos:

<h4 align="left"> Clase PDF </h4>

```python
class PDF(FPDF):
    def __init__(self, title="Report"):
        super().__init__()
        self.title = title
```
Se define la clase base `PDF`, que hereda de `FPDF`, la cual permite construir archivos PDF en Python. En su constructor (`__init__`), se inicializa la clase padre con `super().__init__()` y se guarda el título que se mostrará en el encabezado del documento, por defecto `"Report"`.

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
Este método define el encabezado del PDF. Primero, se configura una fuente Helvetica en negrita de tamaño 14 y se escribe el título centrado. Luego, con una fuente más pequeña (Helvetica 10), se imprime la fecha actual centrada. Se deja un pequeño espacio vertical de 5 unidades después del encabezado.

```python
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
```
Aquí se define el pie de página. Se posiciona el cursor 15 unidades antes del borde inferior, se selecciona una fuente cursiva y pequeña, y se imprime el número de página actual centrado.

```python
    def setup_page(self):
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
```
Este método ayuda a configurar la página al activar el salto automático de página con un margen inferior de 15 unidades y agregar una nueva página.

```python
    def _add_table_header(self, headers, col_widths):
        self.set_font("Helvetica", "B", 10)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, align="C")
        self.ln()
```
Este método interno permite crear la fila de encabezados de una tabla. Usa fuente en negrita y escribe cada celda del encabezado con bordes y alineación centrada, según el ancho especificado por `col_widths`.

```python
    def _add_table_row(self, row_data, col_widths, line_height=8):
        self.set_font("Helvetica", "", 10)
        for i, cell in enumerate(row_data):
            self.cell(col_widths[i], line_height, str(cell), border=1)
        self.ln()
```
Este método agrega una fila de datos a la tabla. Usa fuente normal y recorre cada valor en la fila para escribirlo en una celda con el ancho correspondiente y borde.

```python
    def generate_table(self, headers, rows, col_widths):
        self._add_table_header(headers, col_widths)
        for row in rows:
            self._add_table_row(row, col_widths)
```
Este método permite construir una tabla completa recibiendo encabezados, filas y anchos. Primero escribe la fila de encabezados y luego cada fila de datos.

<h4 align="left"> Clase InventoryReportPDF </h4>

```python
class InventoryReportPDF(PDF):
    def __init__(self):
        super().__init__(title="Inventory Report")
```
Esta clase hereda de `PDF` y representa un reporte del inventario. En su constructor se llama al constructor de la clase base (`PDF`) con un título personalizado: `"Inventory Report"`, que será mostrado en el encabezado de cada página.

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
El método `generate` se encarga de construir el contenido del PDF. Comienza configurando la página y luego define los títulos de columna (`headers`) y el ancho de cada una (`col_widths`). Se inicializa también una lista vacía `rows`, que almacenará cada fila de la tabla.

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
Se recorre cada registro en `records`, y se extrae el producto, su información de inventario (`stock`) y su ubicación. Luego se revisa si el estado del producto incluye una fecha de vencimiento o una condición específica, y se construye la cadena `state_str` de forma adecuada.

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
Con toda la información procesada, se construye una lista que representa una fila en la tabla del PDF y se agrega a `rows`.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
Finalmente, se llama al método `generate_table` (heredado) para construir la tabla y se guarda el archivo PDF con el nombre proporcionado (`inventory_report.pdf` por defecto).

<h4 align="left"> Clase MovementsReportPDF </h4>

```python
class MovementsReportPDF(PDF):
    def __init__(self):
        super().__init__(title="Inventory Movements Report")
```
Esta clase genera un reporte de movimientos de inventario. En su constructor se pasa un título específico a la clase base: `"Inventory Movements Report"`.

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
El método `generate` prepara la página y define los encabezados y anchos de columna. También se inicializa la lista `rows` para almacenar los movimientos.

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
Se recorre cada movimiento y se extrae la información relevante para agregarla como una nueva fila de la tabla.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
Se genera la tabla con los datos y se guarda el PDF bajo el nombre indicado.


<h4 align="left"> Clase BillPDF </h4>

```python
class BillPDF(PDF):
    def generate(self, bill, filename="bill_report.pdf"):
        self.add_page()
        self.set_font("Helvetica", "", 12)
```
Esta clase también hereda de `PDF` y su propósito es generar una factura. A diferencia de otras, no define un constructor propio, por lo que usa el título por defecto `"Report"`. En el método `generate`, se añade una nueva página y se establece el tipo de letra base para el contenido del documento.

```python
        self.cell(0, 10, f"Bill ID: {bill._bill_id}", ln=True)
        self.cell(0, 10, f"Date: {bill.date.strftime('%Y-%m-%d')}", ln=True)
        self.cell(0, 10, f"Entity: {bill.entity.name}", ln=True)
        self.cell(0, 10, f"Type: {bill.entity_type}", ln=True)
        self.cell(0, 10, f"Payment Method: {bill.payment_method}", ln=True)
```
Se imprimen en el PDF varios detalles básicos de la factura: el ID, la fecha, la entidad involucrada (cliente o proveedor), el tipo de entidad y el método de pago.

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
Si el método de pago es en efectivo (`Cash`), se realiza una verificación adicional. Se calcula el total de la factura y el monto entregado. Si el monto es suficiente, se muestra el cambio a entregar; de lo contrario, se indica cuánto dinero hace falta. Esta sección ofrece un control adicional para pagos en efectivo.

```python
        self.ln(5)
```
Se añade un pequeño espacio vertical antes de continuar con la tabla de productos.

```python
        self.set_font("Helvetica", "B", 10)
        headers = ["Code", "Product", "Amount", "Unit Cost", "Subtotal"]
        col_widths = [30, 50, 30, 30, 30]
        self._add_table_header(headers, col_widths)
```
Se establece una fuente en negrita para los encabezados de la tabla y luego se llama a `_add_table_header`, un método heredado que dibuja los encabezados con sus respectivos anchos.

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
Se cambia a una fuente normal para las filas y se recorren los productos de la factura. Por cada uno, se extraen los datos y se genera una fila con código, nombre, cantidad, precio unitario y subtotal (cantidad × precio).

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
Finalmente, se agrega una fila con el total general de la factura. Se hace con una celda que ocupa todas las columnas excepto la última (donde va el valor del total). Luego, se guarda el documento en un archivo PDF con el nombre especificado.

<h4 align="left"> Clase CriticalStockPDF </h4>

```python
class CriticalStockPDF(PDF):
    def __init__(self):
        super().__init__(title="Critic Stock")
```
Esta clase hereda de `PDF` y se utiliza para generar un reporte de productos cuyo stock se encuentra en estado crítico (por debajo del mínimo). En el constructor, llama a la clase base (`PDF`) y define como título `"Critic Stock"`, que se mostrará en el encabezado del PDF.

```python
    def generate(self, records: list, filename="critical_stock.pdf"):
        self.add_page()
```
El método `generate` toma como argumentos una lista de `records` (productos en estado crítico) y el nombre del archivo a generar. Inicia agregando una nueva página al documento PDF.

```python
        headers = [
            "Code", "Product", "Category", "Stock", "Minimum", "Location"
        ]
        col_widths = [20, 45, 30, 20, 25, 50]
```
Se definen los encabezados de la tabla que se va a mostrar en el reporte, junto con los anchos correspondientes para cada columna. La información incluye el código, nombre del producto, categoría, cantidad actual, stock mínimo y ubicación.

```python
        rows = []
        for record in records:
            product = record.product
            stock = record.stock
            location = record.location
```
Se inicializa la lista `rows`, que contendrá las filas de datos. Luego, se recorre cada registro recibido. Se extrae el producto, su información de stock y la ubicación dentro del inventario.

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
Se construye una fila con los datos del producto: el código (accedido como atributo privado), nombre, categoría, stock actual (usando el método `get_actual_stock()`), el mínimo requerido y la ubicación formateada como "Aisle X - Shelf Y". Cada fila se agrega a la lista `rows`.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
Finalmente, se llama al método `generate_table` para renderizar la tabla completa, usando los encabezados, las filas y los anchos definidos. Luego, se guarda el PDF con el nombre proporcionado.

<h4 align="left"> Clase ActorHistoryPDF </h4>

```python
class ActorHistoryPDF(PDF):
    def __init__(self, actor_name, actor_type):
        title = f"History for {actor_type.capitalize()}: {actor_name}"
        super().__init__(title)
```
Esta clase hereda de `PDF` y se utiliza para generar un historial de movimientos realizados por un actor específico del sistema (por ejemplo, un proveedor o un usuario). En el constructor, recibe el `actor_name` y el `actor_type`, y construye dinámicamente el título del reporte con el formato `"History for <ActorType>: <ActorName>"`. Luego pasa ese título a la clase base `PDF` para que sea utilizado como encabezado del documento.

```python
    def generate(self, movements: list, filename="actor_history.pdf"):
        self.setup_page()
```
El método `generate` recibe la lista de movimientos que se desea reportar y el nombre del archivo de salida. Comienza inicializando la página del PDF con `setup_page()`.

```python
        headers = ["Date", "Product", "Code", "Amount", "Type", "Reason"]
        col_widths = [25, 45, 25, 15, 20, 60]
```
Se definen los encabezados para la tabla: fecha, nombre del producto, código, cantidad, tipo de movimiento (entrada o salida), y la razón del movimiento. También se especifican los anchos para cada columna en el PDF.

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
Se crea la lista `rows` para almacenar cada movimiento como una fila de la tabla. Para cada objeto `movement`:

- Se convierte la fecha a formato `YYYY-MM-DD`.

- Se accede al nombre del producto y su código (el cual es privado).

- Se registra la cantidad de producto involucrado (`amount`), el tipo de movimiento (`type`), y la razón (`reason`).

Cada uno de estos datos se agrupa en una fila que se añade a la tabla.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
Finalmente, se llama a `generate_table` para construir visualmente la tabla en el PDF, y se guarda el archivo con el nombre especificado (`actor_history.pdf` por defecto).

<h4 align="left"> Clase SalesSummaryPDF </h4>

```python
class SalesSummaryPDF(PDF):
    def __init__(self, title="Sales Summary Report"):
        super().__init__(title)
```
Esta clase también hereda de `PDF` y está diseñada para generar un informe de resumen de ventas. En el constructor, se puede especificar un título personalizado (por defecto, `"Sales Summary Report"`). Este título es enviado a la clase base `PDF`, y será mostrado automáticamente en el encabezado del documento.

```python
    def generate(self, summary_data: dict, filename="sales_summary.pdf"):
        self.setup_page()
```
El método `generate` toma como entrada un diccionario `summary_data` que contiene el resumen de ventas por producto, y opcionalmente un nombre de archivo para guardar el PDF (`sales_summary.pdf` por defecto). Primero se configura la página llamando a `setup_page()`.

```python
        headers = [
            "Code", "Product", "IN Qty", "IN Cost", "OUT Qty", "OUT Sales"
        ]
        col_widths = [30, 50, 25, 30, 25, 30]
```
Aquí se definen los encabezados de la tabla del reporte. Cada columna representa:

- `Code`: el código del producto.

- `Product`: el nombre del producto.

- `IN Qty`: la cantidad total de unidades ingresadas al inventario.

- `IN Cost`: el costo total de esas entradas.

- `OUT Qty`: la cantidad total de unidades salientes (vendidas o despachadas).

- `OUT Sales`: el valor de esas salidas.

También se definen los anchos de las columnas para que se distribuyan de forma proporcional y clara en el PDF.

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
Se construyen las filas de la tabla recorriendo el diccionario `summary_data`, donde cada clave `code` representa un producto. Se extraen los valores asociados, que deben incluir:

- El nombre del producto (`data["name"]`),

- La cantidad y el costo total de las entradas (`data["in"]["qty"]` y `data["in"]["cost"]`),

- La cantidad y el valor de las salidas (`data["out"]["qty"]` y `data["out"]["cost"]`).

Los valores monetarios se formatean con dos decimales usando `f"${valor:.2f}"`.

```python
        self.generate_table(headers, rows, col_widths)
        self.output(filename)
```
Finalmente, se llama a `generate_table` para renderizar los encabezados y filas en el PDF, y luego se guarda el archivo con `self.output(filename)`.

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
El archivo inicia con una serie de importaciones que traen los módulos y clases necesarias para que el sistema funcione. Estas incluyen la clase base `Inventory`, las clases que modelan productos, ubicaciones, stocks y movimientos, así como los componentes encargados de la generación de facturas, reportes y extractos en PDF.


```python
class System(Inventory):
    def __init__(self):
        super().__init__()
        self.bills = {}
        self.customers = {}
        self.suppliers = {}
```
Luego se define la clase `System`, que hereda de `Inventory`. En su constructor (`__init__`) se llama al inicializador de la clase base con `super()` y se crean tres diccionarios vacíos: `bills`, `customers` y `suppliers`. Estos almacenarán las facturas, clientes y proveedores registrados respectivamente.

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
El método `entry_record` permite registrar un nuevo producto en el inventario. Primero, verifica si el producto ya existe; si no, le asigna una ubicación automática según su categoría, crea un objeto `Stock`, lo envuelve todo en un `InventoryRecord`, y lo añade al sistema. También se registra el movimiento de entrada con `Movement`.


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
El método `make_sale` gestiona una venta. Verifica que el producto exista, obtiene el registro del inventario y crea un movimiento de salida. Antes de ejecutarlo, comprueba si hay suficiente stock disponible. Si la validación pasa, se añade el movimiento.

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
Los métodos `add_customer` y `add_supplier` permiten registrar nuevos actores en el sistema. Verifican si el ID del cliente o proveedor ya existe, y si no, los agregan.

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
Los métodos `generate_customer_history` y `generate_supplier_history` permiten obtener una lista de movimientos asociados a un cliente o proveedor. Filtran los movimientos registrados según el ID y tipo de actor.

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
El método `create_bill` genera una factura a partir de una lista de movimientos. Verifica que los movimientos pertenezcan al mismo actor, agrega los productos al objeto `Bill` y guarda su referencia. Finalmente, intenta realizar el pago con el método de pago correspondiente.

```python
    def export_full_system(self, path="full_backup.json"):
        Extracts.export_full_system(self, path)

    def load_full_backup(self, path="full_backup.json"):
        Extracts.load_full_backup(path, self)
```
Los métodos `export_full_system` y `load_full_backup` permiten exportar o importar un respaldo completo del sistema a un archivo `.json`, utilizando la clase `Extracts`.

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
A continuación, se encuentran los métodos para generar diferentes tipos de reportes en formato PDF. Por ejemplo, `export_inventory_pdf` genera un reporte de inventario, `export_movements_pdf` uno de movimientos, y `export_bill_pdf` una factura individual.

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
El método `export_critical_stock_pdf` genera un reporte de los productos que están por debajo de su stock mínimo. Si no hay ningún producto crítico, se imprime un mensaje.

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
El método `export_actor_history_pdf` genera un historial de movimientos para un actor (cliente o proveedor). Detecta su tipo, filtra los movimientos y genera el PDF correspondiente.

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
Finalmente, el método `export_sales_summary_pdf` genera un resumen de ventas y compras, mostrando entradas (compras) y salidas (ventas) por cada producto. Se puede filtrar por código de producto.









---------

Importamos la biblioteca `tkinter` como `tk`, y de esta misma importamos los módulos `filedialog`, `messagebox`, `Toplevel`, `StringVar`, `OptionMenu` y `ttk`

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









