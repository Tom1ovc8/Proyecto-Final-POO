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

<h3 align="center"> Inventory_Management </h3>

-----------

<h3 align="center"> Operations_Center </h3>

-----------

<h3 align="center"> People </h3>

#### Customer:

```pyton import uuid

class Customer:
    def __init__(self, name, number_id, customer_id=None):
        self.name = name
        self.number_id = number_id
        self._id = customer_id if customer_id else str(uuid.uuid4())

    def to_dict(self):
        return {
            "name": self.name,
            "number_id": self.number_id,
            "_id": self._id
        }
```

-----------

<h3 align="center"> Products </h3>

-----------

<h3 align="center"> Transactions </h3>

