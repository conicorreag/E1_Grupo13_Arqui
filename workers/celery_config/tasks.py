# celery
from celery import shared_task
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime



@shared_task
def make_prediction(data):
    # reques_data = {historial: [{fecha: fecha, precio: precio}], N: 3}
    # {historial: [{fecha: 1/2/5, precio: 1}, {fecha: 132/5, precio: 12}], N: 3}

    historial = data.get("historial")
    fechas = [entry["fecha"] for entry in historial]
    precios = [entry["precio"] for entry in historial]

    fechas = [(datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.strptime(fechas[0], "%Y-%m-%dT%H:%M:%S.%fZ")).days for fecha in fechas]
    fechas = np.array(fechas)

    precios = np.array(precios)

    # Reshape para que las fechas sean un arreglo bidimensional
    fechas = fechas.reshape(-1, 1)

    # Crear el modelo de regresión lineal
    modelo = LinearRegression()
    modelo.fit(fechas, precios)


    # Realiza predicciones
    lista_ys = modelo.predict(fechas).tolist()  # Convierte el ndarray a una lista

    # ponderador
    N = int(data.get("N"))
    ponderador = 1 + ((5 + N - 50) / 50)

    # prediccion: multiplicar cada elemento de la lista por el ponderador
    prediccion = [y * ponderador for y in lista_ys]  # Aplica el ponderador

    return prediccion