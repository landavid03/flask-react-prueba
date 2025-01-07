
# Sistema de Gestión de Inventario

API/REST para gestionar el inventario de una cadena de tiendas minoristas con frontend basico.





## Instalación

Descargar docker y docker compose

Para verificar la Instalación utiliza

 ``` docker --version ```

 ``` docker-compose --version ```

Construye y levanta los servicios:

 ``` docker-compose up --build -d ```

Verifica para el backend

http://localhost.com:5000/api/docs

Verifica para el front

http://localhost.com:5173

## Tech Stack

**Frontend:** React

**Backend:** Flask, Python, Postgresql





## API Reference
### Products
#### Obtener productos

```http
  GET /api/products
```

#### Obtener producto por ID

```http
  GET /api/products/${id}
```

#### Crear producto

```http
  POST /api/products
```

#### Actualizar producto por ID

```http
  PUT /api/products/${id}
```

#### Eliminar producto por ID

```http
  DELETE /api/products/${id}
```

### Stock
#### Obtener inventario

```http
  GET /api/stores/${id}/inventory
```

#### Crear inventario

```http
  POST /api/stock
```

#### Transferir inventario

```http
  POST /api/inventory/transfer
```

#### Alertas

```http
  GET /api/inventory/alerts
```

