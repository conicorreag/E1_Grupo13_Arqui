import paho.mqtt.client as mqtt
import requests
import json
import time
from dotenv import load_dotenv
import os
load_dotenv()


HOST = os.getenv("HOST")
PORT = 9000
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
TOPIC = [("stocks/info", 0), ("stocks/validation", 0)]


GROUP_ID = 13
POST_URL = "http://fastapi_app:8000/create_stocks/"
PATCH_URL = "http://fastapi_app:8000/transactions/"


# Espera hasta que la API de FastAPI esté disponible
def wait_for_fastapi(api_url):
    max_retries = 30  # Número máximo de intentos de conexión
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                print("FastAPI está listo para recibir conexiones.")
                break
        except requests.exceptions.RequestException:
            pass

        print("Esperando a FastAPI...")
        retries += 1
        time.sleep(2)  # Esperar 2 segundos antes de intentar nuevamente

    if retries == max_retries:
        print("No se pudo conectar a FastAPI después de varios intentos.")

# Llamar a la función para esperar a FastAPI


# Callback que se ejecuta cuando se conecta al broker

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker con código:", rc)
    client.subscribe(TOPIC)

# Callback que se ejecuta cuando se recibe un mensaje


def on_message(client, userdata, msg):
    msg_topic = msg.topic
    print(f"Mensaje recibido en el canal {msg.topic}")

    if msg_topic == "stocks/info":
        print(msg.payload.decode())
        response = requests.post(POST_URL, json=msg.payload.decode())
        print(response)

    elif msg_topic == "stocks/validation":
        data = json.loads(msg.payload.decode())
        if data["group_id"] == GROUP_ID:
            print("Received Our Request Validation")
            response = requests.patch(PATCH_URL, data=json.dumps(data), headers={'Content-type': 'application/json'})
        else:
            print(f"Ignored Group {data['group_id']}'s Request")



# Crear un cliente MQTT
client = mqtt.Client()
client.username_pw_set(USER, PASSWORD)

# Asignar las funciones de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectarse al broker
client.connect(HOST, PORT, keepalive=60)

# Iniciar el bucle para mantener la conexión y procesar los mensajes
client.loop_forever()
