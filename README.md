### Documentación E2 grupo 13

### RDOC1 Diagrama Anexo

El diagrama se encuentra en la misma carpeta docs.

### RDOC2 Integración con WebPay

Para realizar la integración con Webpay, se siguieron los siguientes pasos:

1. Importar modulo transbank-sdk y añadirlo a requirements.txt 
2. Crear Funcion webpay_plus_create() que con el metodo transactions.create crea una transaccion en webpay y retorna URL de pago de webpay y token. 
3. Crear Función webpay_commit() con transactions.commit de la librería Transbank encargada de confirmar y devuelve el estado de la transacción. 
4. Crear transacción con webpay_plus_create.
5. Añadir vista en frontend con formulario encargado de redirigir a URL entregado, pasando token como valor. 
6. Añadir vista al frontend encargada de recibir al usuario luego de pagar en webpay y además recibir token entregado, este puede ser token_ws o tbk_token dependiendo del flujo de pago.   
7. Revisar el estado de la transacción en el backend mediante la funcion webpay_commit y en el caso de ser exitoso, descontar dinero de wallet de usuario

### RDOC3 Aplicación en Serverless

No se realizó este requisito ni la función lamda.

### RDOC4 Llamadas a la API 

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

