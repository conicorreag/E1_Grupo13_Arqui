### Documentación E2 grupo 13

### RDOC1 Diagrama Anexo

El diagrama se encuentra en la misma carpeta docs.

### RDOC2 Flujos configueración IaaC

A continuación se explica el flujo de la configuración de terraform.

**Configuración instancia EC2, Grupo de Seguridad e IP Elástica**

1. En primer lugar, se especifica el proveedor necesario y su versión. En este caso, es AWS con una restricción de versión.
2. Luego se define el proveedor AWS y se especifica la región de AWS como us-east-1. En esta región se crearán los recursos de AWS.
3. A continuación, se genera una clave privada RSA que se utilizará para SSH.
4. Se crear un par de claves AWS llamadas "iaac" usando la clave pública generada en el paso anterior.
5. Se define un grupo de seguridad que permite el tráfico SSH entrante en el puerto 22 desde cualquier origen y permite todo el tráfico saliente.
6. Se crea una instancia EC2 deAWS con atributos específicos. Estos son
    - **ami**: La ID de la Amazon Machine Image (AMI).
    - **instance_type**: El tipo de instancia EC2, en este caso t2.micro.
    - **key_name**: El nombre del par de claves SSH.
    - **vpc_security_group_ids**: ID(s) del grupo de seguridad asociado(s) con la instancia.
    - **user_data**: El contenido del script (deployment.sh) que se ejecutará al lanzar la instancia. Este script automatiza la instalación de Docker, donde primer configura el sistema para usar el repositorio de Docker y luego instala Dcoker.
    - **tags**: Etiquetas asociadas con la instancia EC2.
7. Se asocia una IP elástica con la instancia EC2 creada anteriormente.
8. Finalmente, se tienen una salidas que proporcionan información útil después de que se ejecuta el script de Terraform. Muestra la IP elástica y el comando SSH para conectarse a la instancia EC2 creada.

**Configuración instancia API Gateway**

1. En primer lugar, se establece la región de AWS en us-east-1.
2. Luego sefine un recurso terraform_remote_state para acceder al estado remoto del proyecto de Terraform de la instancia EC2 y componentes relacionados.
3. A continuación, se define una API Gateway HTTP con el nombre my-api.
4. Se definen dos integraciones para los métodos GET y POST de la API Gateway. La URL de integración se toma del estado remoto de Terraform del proyecto EC2.
4. Se definen rutas para los métodos GET y POST en la API Gateway, apuntando a las integraciones correspondientes.
5. Se define una etapa llamada "prod" que está asociada a la API Gateway. La configuración es para el despliegue automático.
6. Finalmente, Se define una salida que devuelve la URL de invocación de la etapa prod.

### RDOC3 Llamadas a la API 

A continuación se detallan las llamadas a la API realizadas desde el frontend:

- **(POST) g13arquitectura.me/create_prediction/ :** Crea una predicción en la base de datos, recibe un json con los datos de la predicción y retorna un json con las fechas y precios futuros calculados.

```json
{
  "final_date": "predictionDate",
  "quantity": "cantidad",
  "symbol": "symbol",
  "user_sub": "user.sub"
}
```

- **(GET) g13arquitectura.me/job_heartbeat/ :** Recibe un json con el estado de un job y lo actualiza en la base de datos, para mostrar el estado de la página principal

- **(GET) g13arquitectura.me/stocks/ :** Retorna un json con los datos de las acciones de la bolsa de valores recibidas desde el broker.

- **(GET) g13arquitectura.me/stocks/{symbol} :** Retorna un json con los precios históricos del stock con el símbolo seleccionado.

- **(POST) g13arquitectura.me/transactions/ :** Recibe desde el front la cantidad y el símbolo de la acción a comprar, y retorna un json con el estado de la transacción.

EJEMPLO DE JSON A ENVIAR:

```json
{
  "user_sub": "user_sub",
  "datetime": "datetime",
  "symbol": "symbol",
  "quantity": "quantity"
}
```

- **(GET) g13arquitectura.me/transactions/{user_sub} :** Retorna el listado de las transacciones históricas realizadas por el usuario.

- **(POST) g13arquitectura.me/transactions_webpay/ :** Recibe desde el front el token de la transacción y un bool que indica si fue anulada o no por el usuario.

EJEMPLO DE JSON A ENVIAR:

```json
{
  "token": "token",
  "is_tbk": "anulada"
}
```

- **(GET) g13arquitectura.me/user_predictions/{user_sub} :** Retorna el detalle de las predicciones históricas realizadas por el usuario.

- **(PUT) g13arquitectura.me/wallet/ :** Recibe desde el front la cantidad de dinero a añadir en la billetera virtual.

EJEMPLO DE JSON A ENVIAR:

```json
{
  "user_sub": "user.sub",
  "amount": "parseFloat(monto)"
}
```

- **(GET) g13arquitectura.me/wallet/{user_sub} :** Retorna el saldo de la billetera virtual del usuario.

