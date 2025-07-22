<h1 align="center"> Gestión de Inventarios </h1>

<h2 align="center"> Proyecto Final POO </h2>

El objetivo principal de este proyecto es hacer una aplicación que emula un sistema de gestión de inventario para una bodega por medio de una interfaz gráfica de usuario (GUI).
El programa tiene operaciones que podemos realizar como:
  - Crear objeto a almacenar  
  - Operaciones de registro de entrada y salida
  - Método para obtener listado de inventario actual
  - Manejo de fechas en los registros

Y adicional a eso, tenemos características extras como:
  + Carga masiva de registros
  + Manejo de archivos para persistencia de datos
  + Generación de reportes en forma de documentos

<h2 align="center"> Índice </h2>

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

El método `add_record` recibe la instancia `record`, del cual tomaremos el codigo del producto como la variable `code`. La función `add_record` se encargara de revisar si el código de dicho producto ya esta o no esta en el diccionario de registros `records`. Si el código no está, se realizara el registro correctamente, pero si el código ya esta previamente en el diccionario de registros, el sistema arroja el mensaje *”This product already exists in the inventory”*.

```python
    def add_record(self, record):
        code = record.product.code
        if code not in self.records:
            self.records[code] = record
        else:
            print("This product already exists in the inventory.")
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

Creamos una clase `InventoryApp`, en la cual vamos a definir absolutamente todo lo que tiene que ver con la interfaz grafica (GUI). Definimos el constructor `__init__` con las instancias `root` y `system`, y le damos el título `Inventory Management System` a nuestra aplicación. También especificamos el estilo a usar y el tamaño de la interfaz.

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

Para crear un botón, es necesario mandarle los parámetros `main_frame`, `text` y `command`, es decir, que tamaño va a tener cada botón, que va a decir cada uno, y que función va a tener. Se especifican las márgenes y se hace posible ser expandir el texto al expandir la interfaz.

```python
        for i, (text, command) in enumerate(buttons):
            ttk.Button(
                main_frame, text=text, command=command
            ).pack(pady=6, fill="x")
```

Definimos la función `load_json`, la cual vamos a utilizar para carcar el archivo .JSON donde vamos a tener las bibliotecas de datos. Este nos va a permitir abrir el explorador de archivos para añadir nuestro archivo especificamente .JSON. Si la ruta del archivo es correcta, se hara backup correctamente y aparecerá un messagebox con el mensaje `"Success", "JSON archive has been loaded"`. En caso de que salga un error, el mensaje sera `"Error", "Couldn't load the archive"` y nos especificara el tipo de error ocurrido.

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

Se generará tambien otro campo llamado `"Select State type:"` en donde se crearán dos botones llamados `State` y `Expiration Date`. De estos solo se podra elegir uno a la vez, y nos permitirán ingresar el estado del producto al momento de ser ingresado al inventario, ya sea su estado fisico, o su fecha de expiración según corresponda. Estos valores se almacenaran con las claves `condition` y `date` respectivamente.

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

Se define la función `update_state_fields()` para que, en caso de que elijamos ingresar la condición del producto, el menú de fechas de expiración se oculte, y viceversa.

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

Continuando con el campo de proveedores, en caso de que se haya elegido `existent`, se toman los proveedores del diccionario uno por uno y el nombre se guarda en la variable `supplier`. En caso de que se haya elegido `new`, se verifica que los campos `supplier_name` y `supplier contact` hayan sido diligenciados, en caso de que no, retorna el error `"You must enter the supplier name and contact"`. Se verifica tambien que el `supplier_contact` sea un valor numerico, y en caso de que no, retorna el mensaje `"The contact number must be numeric only"`.

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

Definimos la función `export_to_json` para abrir guardar el archivo .JSON con el nombre `"Save Backup"`. Si la ruta seleccionada por el usuario es correcta, se genera un messagebox con el mensaje `"Success", "Backup saved in:"` y especifica la ruta seleccionada. En caso de que ocurra algún error, se genera un messagebox con el mensaje `"Error", "Couldn't export"` y especificando el error ocurrido.

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

Definimos la función `add_movement_method`

Definimos la función `créate_bill_method`

Definimos la función `export_movements_report`

Definimos la función `export_bill`

Definimos la función `generate_sales_summary`

Definimos la función `show_restock_suggestions`

Definimos la función `simple_input_dialog`







