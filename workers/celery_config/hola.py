import json
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.pyplot as plt

request_data = {"historial": [{"fecha": "2020-05-01", "precio": 1000}, {"fecha": "2020-08-23", "precio": 2050}, {"fecha": "2020-10-15", "precio": 40}]}

# Suponiendo que tienes un JSON válido en request_data
historial = request_data.get("historial")
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
predicciones = modelo.predict(fechas)

# # Dibuja el gráfico de dispersión y la línea de regresión
plt.plot(fechas, precios, 'o-', label='Datos reales', markersize=8)
plt.plot(fechas, predicciones, color='red', label='Línea de regresión')
plt.xlabel('Fechas')
plt.ylabel('Precios')
plt.legend()
plt.show()

print(predicciones)