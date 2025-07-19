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

#### Stock:



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

-----------

<h3 align="center"> Transactions </h3>

