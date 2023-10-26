import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

def calcular_prediccion(data):
    historial = data.get("historial")
    fechas = [entry["fecha"] for entry in historial]
    precios = [entry["precio"] for entry in historial]

    fechas = [(datetime.strptime(fecha, "%Y-%m-%d") - datetime.strptime(fechas[0], "%Y-%m-%d")).days for fecha in fechas]
    fechas = np.array(fechas)

    precios = np.array(precios)

    # Reshape para que las fechas sean un arreglo bidimensional
    fechas = fechas.reshape(-1, 1)

    # Crear el modelo de regresión lineal
    modelo = LinearRegression()
    modelo.fit(fechas, precios)

    # Realiza predicciones
    lista_ys = modelo.predict(fechas)
    
    #ponderador
    N = int(data.get("N"))
    ponderador = 1 + ((5 + N - 50) / 50)

    #prediccion: multiplicar cada elemento de la lista por el ponderador
    prediccion = lista_ys * ponderador
    return prediccion
    
