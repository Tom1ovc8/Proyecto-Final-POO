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

-----------

<h3 align="center"> Class Diagram </h3>

-----------

<h3 align="center"> Inventory_Management </h3>

#### Inventory Record:

En la clase `InventoryRecord`, por medio del método `__init__` se definen los atributos que va a tener el registro de nuestro inventario, como serían: `product`, `stock` y `location`.

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

#### Inventory:

En la clase `Inventory` definimos dos atributos donde almacenaremos datos, que se crean directamente desde el objeto sin necesidad de recibirlos como parámetro. Estos son: `self.records` que es un diccionario vacío, y `self.movements` que es una lista vacía.

```python
class Inventory:
    def __init__(self):
        self.records = {}
        self.movements = []
```

Al método `add_record` le definimos un atributo `record`, el cual usaremos posteriormente para crear el registro de código de un producto (esta acción la llamamos `code`). La función `add_record` se encargara de revisar si el código de dicho producto ya esta o no esta en el diccionario de registros `records`. Si el código no está, se realizara el registro correctamente, pero si el código ya esta previamente en el diccionario de registros, el sistema arroja el mensaje *”This product already exists in the inventory”*.

```python
    def add_record(self, record):
        code = record.product.code
        if code not in self.records:
            self.records[code] = record
        else:
            print("This product already exists in the inventory.")
```

Definimos la función `get_record`, la cual nos servirá para consultar el código de algún producto registrado previamente en el diccionario `records`. En caso de que el código no exista en el diccionario, retorna `None`.

```python
    def get_record(self, code):
        return self.records.get(code)
```

Se definió la función `remove_record` para, como lo dice su nombre, poder remover el registro de código de un producto por medio de la instrucción `del`. La función va a buscar el código de la biblioteca de registros. Si se encuentra el código, se procede con la función correctamente y se elimina el registro de la biblioteca. Si el código no se encuentra, el sistema arroja el mensaje “*No record found with this code*”.

```python
    def remove_record(self, code):
        if code in self.records:
            del self.records[code]
        else:
            print("No record found with this code.")
```

Cada cambio de cantidad (definido como `movement`), ya sea ingreso o salida de productos, se almacenará en la lista de movimientos con el comando `self.movements.append(movement)`. El comando `product_code` se define como el código del producto del movimiento. `delta` se define como el cambio de cantidad de inventario de los productos, ya sea positivo o negativo. Posteriormente se actualiza el stock mediante el comando `self.records[product_code].stock.update_stock(delta, movement)`, que toma el código del producto y el método `update_stock()` de `stock` es el que se encarga de actualizar el inventario del producto. 

```python
    def add_movement(self, movement):
        self.movements.append(movement)
        product_code = movement.product.code
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

El método `generate_stock_report` genera un reporte (`report` que es una lista vacía) del estado actual del inventario, producto por producto. Para cada producto guardado en el diccionario de registros, el método agrega un diccionario con los datos del producto: `”Name”` (nombre del producto), `”Code”` (código del producto), `”Current Stock”` (stock actual del producto) y `”Status”` (estado en el que se encuentra el stock del producto: *Suficiente, bajo o agotado*, según el mínimo y máximo establecido).

```python
    def generate_stock_report(self):
        report = []
        for record in self.records.values():
            product = record.product
            stock = record.stock
            report.append({
                "Name": product.name,
                "Code": product.code,
                "Current Stock": stock.get_actual_stock(),
                "Status": stock.check_stock()
            })
        return report
```

El método `restock_suggestions` sugiere que productos necesitan ser reabastecidos según el mínimo establecido, es decir que tienen stock por debajo de este. Este revisa producto por producto y su estado de stock e identifica si esta o no por debajo del mínimo. En caso de que si lo esté, crea una lista de sugerencias vacía `suggestions` donde va a agregar los productos que necesitan el restock con la siguiente información: `”Name”` (nombre del producto), `”Code”` (código del producto), `”Current Stock”` (stock actual del producto), y `”Minimum Required”` (el mínimo necesario de stock definido como `record.stock.minimum_stock`).

```python
    def restock_suggestions(self):
        suggestions = []
        for record in self.records.values():
            if record.stock.check_stock() == "Stock is below the minimum.":
                suggestions.append({
                    "Name": record.product.name,
                    "Code": record.product.code,
                    "Current Stock": record.stock.get_actual_stock(),
                    "Minimum Required": record.stock.minimum_stock
                })
        return suggestions
```

#### Location:

Creamos la clase `Location` a la cual le vamos a asignar unos atributos privados que están fuera del constructor y son compartidos entre todas las instancias de la clase. Estos son `_category_aisles` que es la categoría de cada uno de los pasillos y es un diccionario vacío; `_next_aisle_number` que dicta cual será el siguiente pasillo pasando de uno en uno; `_shelf_counter_by_category` que cuenta cuantos estantes ya han sido asignados por categoría (también es un diccionario vacío).

```python
class Location:
    _category_aisles = {}
    _next_aisle_number = 1
    _shelf_counter_by_category = {}
```

Definimos los atributos de nuestra clase `Location`, los cuales son `aisle` (pasillos) y `shelf` (estantes).

```python
    def __init__(self, aisle, shelf):
        self.aisle = aisle
        self.shelf = shelf
```

Con el decorador `@classmethod` indicamos que el programa trabaja con la clase completa y no solo con objetos individuales. Definimos el método `assign_location` con `cls` en vez de `self`, es decir que puede modificar y acceder a los atributos de clase. Si la instancia de categoría `category` no tiene un pasillo asignado, se le asignara uno disponible, de forma que si hay un pasillo ocupado, se revisara el siguiente hasta que se encuentre uno disponible.

```python
    @classmethod
    def assign_location(cls, category):
        if category not in cls._category_aisles:
            cls._category_aisles[category] = cls._next_aisle_number
            cls._next_aisle_number += 1
```

Ahora se van a contar estantes para esa categoría. Si es la primera vez que aparece esa categoría, el contador inicia en 0, y luego se incrementa de uno en uno para asignar un nuevo estante. Luego retorna el numero de pasillo y de estante de dicho producto por medio de `cls(aisle, shelf)`.

```python
        aisle = cls._category_aisles[category]
        cls._shelf_counter_by_category.setdefault(category, 0)
        cls._shelf_counter_by_category[category] += 1
        shelf = cls._shelf_counter_by_category[category]
        return cls(aisle, shelf)
```

Definimos el método `set_shelf` que permite cambiar únicamente el número de estante del producto por otro en el mismo pasillo.

```python
    def set_shelf(self, shelf):
        self.shelf = shelf
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

Definimos el método `check_stock`, con el que vamos a comparar el stock actual de un producto con el stock mínimo definido. Si el stock actual es menor al stock mínimo, nos retorna el mensaje `”Stock is below the minimum”`. SI el stock actual es mayor al stock máximo, nos retorna el mensaje `”Stock excedes the maximum”`. En caso de que el stock este entre el mínimo y el máximo, nos retorna el mensaje `”Stock is within an aceptable range”`.

```python
    def check_stock(self):
        if self._actual_stock < self.minimum_stock:
            return "Stock is below the minimum."
        elif self._actual_stock > self.maximum_stock:
            return "Stock exceeds the maximum."
        else:
            return "Stock is within an acceptable range."
```

Se define el método `is_valid_update` con un atributo `delta` que representa el cambio de stock. El método revisa que antes de que se modifique el stock, el cambio no deje el stock ni por debajo del mínimo, ni por encima del máximo permitido.

```python
    def is_valid_update(self, delta):
        new_stock = self._actual_stock + delta
        return 0 <= new_stock <= self.maximum_stock
```

El método `update_stock` se define para actualizar el stock de un producto. Por medio de este método, si la actualización del stock no es válida, retornara el mensaje `”Cannot update stock”`. En caso de que si sea válida, se sumara el movimiento `delta` al stock actual ya sea entrada o salida. Si se paso un movimiento, se guarda en el diccionario de registros, si no, retorna el mensaje `”Only Movement instances are allowed to update stock”`.

```python
    def update_stock(self, delta, movement = None):
        if not self.is_valid_update(delta):
            print("Cannot update stock.")
            return False
        self._actual_stock += delta
        if movement:
            if isinstance(movement, Movement):
                self._record.append(movement)
            else:
                raise TypeError("Only Movement instances are allowed to update stock.")
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

Se define el método `show_history` para que se imprima toda la lista de movimientos en forma de diccionario.

```python
    def show_history(self):
        for stock_record in self._record:
            print(stock_record.to_dict())        
```

El método `to_dict` retorna el stock actual, el stock mínimo y el stock máximo en diccionario con las claves `actual_stock`, `mínimum_stock` y `máximum_stock`.

```python
    def to_dict(self):
        return {
            "actual_stock": self._actual_stock,
            "minimum_stock": self.minimum_stock,
            "maximum_stock": self.maximum_stock
        }       
```

-----------

<h3 align="center"> Operations_Center </h3>

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
        self._id = supplier_id if supplier_id else str(uuid.uuid4())
        self.name = name
        self.contact_number = contact_number
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

<h3 align="center"> Products </h3>

#### Bills:
Este módulo permite gestionar facturas de compras o ventas, asociadas a una entidad (ya sea un cliente o un proveedor), con una lista de productos, sus cantidades, precios y el método de pago correspondiente.

#### BillItem:
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

#### Card(Payment):
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

#### Cash(Payment):
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

-----------

<h3 align="center"> Transactions </h3>

