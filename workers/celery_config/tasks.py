# celery
from celery import shared_task
from celery_config.controllers import sum_to_n

# standard
import time
from controllers import calcular_prediccion

# The "shared_task" decorator allows creation
# of Celery tasks for reusable apps as it doesn't
# need the instance of the Celery app.
# @celery_app.task()


@shared_task
def make_prediction(request_data):
    # reques_data = {historial: [{fecha: fecha, precio: precio}], N: 3}
    # {historial: [{fecha: 1/2/5, precio: 1}, {fecha: 132/5, precio: 12}], N: 3}

    #lista de predicciones
    return calcular_prediccion(request_data)