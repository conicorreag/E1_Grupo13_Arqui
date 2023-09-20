import paho.mqtt.client as mqtt
import configparser
import requests
import json
import time

# Leer las Credentials desde el archivo usando configparser
config = configparser.ConfigParser()
config.read("credentials.secret")

HOST = config.get("Credentials", "HOST")
PORT = 9000
USER = config.get("Credentials", "USER")
PASSWORD = config.get("Credentials", "PASSWORD")
TOPIC = "stocks/validation"
GROUP_ID = "13"


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
    message = msg.payload.decode()
    if message["group_id"] == GROUP_ID:
        print(f"Mensaje recibido en el canal {msg.topic}")
        api_url = "http://fastapi_app:8000/create_stocks/"
        response = requests.post(api_url, json=message)
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