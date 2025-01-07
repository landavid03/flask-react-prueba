
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



Para ejecutar el codigo de manera independiente debes correr los siguientes comandos:

Backend :
```bash
  flask run app
```
Frontend:
```bash
  npm run dev
```



## Tech Stack

Se decidio hacer uso de flask ya que se necesitaba un microframework ligero y flexible que te permita construir una API REST de manera rápida y simple, sin la sobrecarga de funcionalidades que podrías no necesitar. A diferencia de Django, que es un framework completo con su propio ORM, sistema de administración y muchas características preconfiguradas, Flask te permite añadir solo los componentes que necesites, lo que resulta en una aplicación más liviana y con mejor rendimiento. Esta flexibilidad es especialmente valiosa cuando estás construyendo microservicios o APIs que se integrarán con un frontend en React, ya que no necesitas todas las capacidades de renderizado de templates y manejo de formularios que Django ofrece por defecto.

Elegí Google Compute Engine (GCE) como base para el despliegue en GCP porque es una solución flexible y ampliamente utilizada para alojar aplicaciones, con las siguientes ventajas:
    
- Control total
- Compatibilidad con Docker
- Ideal para alojar aplicaciones completas (Backend, Frontend)
- Compatible con SQL Admin (En caso de tener base de datos independediente al contenedor)
- Altamente escalable en recursos
- Alta disponibilidad

No se uso Cloud Run debido a que es para aplicaciones "serverless" y puede ser una limitante para persistencia de datos


#### Tecnologias usadas: 

**Frontend:** React

**Backend:** Flask, Python, Postgresql


#### Diagrama Arquitectura: 

<img width="587" alt="image" src="https://github.com/user-attachments/assets/fecaa512-5e81-4f0e-acdf-25c7371e8015" />



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

### Swagger UI

Adicional a esto se puede obtener la documentacion entrando a Swagger 

  http://localhost:5000/api/docs/#/default

  <img width="1417" alt="image" src="https://github.com/user-attachments/assets/bca851f8-f410-46aa-ac5b-49e4fa7593f8" />


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`FLASK_ENV=development`


`POSTGRES_USER=postgres`

`POSTGRES_PASSWORD=postgres`

`POSTGRES_DB=deacero`

`DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}`


## Deployment

### Manual

Para hacer el deploy es necesario contar con una cuenta activa en GCP y activar "Compute Engine API"

Los pasos son los siguientes: 

- 1.-  Crear un instancia de Compute Engine y configurarla con la memoria y procesador requeridos y usar una distribucion de linux como Ubuntu

- 2.- Entrar mediante SSH a la VM

- 3.- Actualizar los paquetes 

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

- 4.- Descargar Docker y Docker Compose

    ```bash
    sudo apt install docker.io -y
    ```

    ```bash
    sudo apt install docker-compose -y
    ```

- 5.- Agregar el usuario al grupo de docker

    ```bash
    sudo usermod -aG docker $USER
    ```

- 6.- Clonar el repo en la vm 
    ```bash
    git clone https://github.com/landavid03/flask-react-prueba.git
    ```

- 7.- Agregar las variables de entorno en un archivo .env en la raiz

- 8.- Contruir y levantar los servicios
    ```bash
    docker-compose up --build -d
    ```


### Script

Ejecutar el script llamado despliegue.sh y automaticamente se ejecutara y comenzara a desplegarse el proyecto.
Se debe tener instalado Gcloud GLI
    
    ./despliegue.sh
    
## Running Tests



### Test unitarios e integracion
Para ejecutar las pruebas unitarias es necesario tener pytest y ejecutar los siguientes comandos: 

#### Ejecutar test

```bash
   pytest ./test
```


#### Generar reporte de covertura

```bash
   pytest --cov --cov-report=html:coverage_re  
```

#### Datos del reporte: 

<img width="740" alt="image" src="https://github.com/user-attachments/assets/2c1a5666-56f8-4bc4-bb8a-89a3e4cff44d" />



### Test carga: 
Los test de carga se realizaran mediante locust, es necesario ejecutar este comando el cual iniciara un servidor local donde podremos poner el numero de peticiones y usuarios que se quieren enviar por un tiempo determinado.


```bash
locust -f test_carga.py --host=http://localhost:5000
```

### Pruebas con Postman

Importar la coleccion en postman y ejecutar cada uno de los endpoints para probarlos
## Demo

Frontend:
    
- http://34.51.3.199:5173/

Backend: 

- http://34.51.3.199:5000/api/products
