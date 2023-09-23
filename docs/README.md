## Documentación E1 grupo 13

### RDOC02: Continous Integration

El Continous Integration solamente se implementó en el backend. Este archivo se ejecuta cuando se hace un pull request hacia el main. Para esto se ejecutan los siguientes pasos:

 1. Se clona o verifica el código fuente del repositorio en la máquina virtual donde se ejecuta el trabajo a través de la acción Github Actions. 
 2. Se configura el entorno de Python también a través de una acción predefinida de Github Actions. Para esto se usa la versión 3.10.12 de Python.
 3. Se instalan las dependencias contenidas en el archivo requirements.txt con el comando ```pip install -r requirements.txt```.
 4. Se corre el linter descargado que en este caso es flake8 para Python. Este realiza un análisis estático del código para mejorar la calidad de este. Se hace a través del comando ```flake8 .```.
 5. Se ejecuta un test trivial definido en el backend. Esto se hace mediante pytest que se ejecuta a través de ```pytest```.

 Si todos estos pasos se cumplen correctamente se da la opción de hacer el pull request del main que se hace, por ejemplo, cada vez que se hace merge a este.



### RDOC03: App

Para correr la aplicación de ***manera local*** se deben seguir los siguientes pasos:
**Backend:**

-	Clonar repositorio https://github.com/conicorreag/E1_Backend_Grupo13_Arqui
-	En el terminal, correr pip install -r requirements.txt para asegurarse de tener todas las dependencias necesarias.
-	Crear un .env con las credenciales:

        DB_USER=conicorrea
        DB_PASSWORD=calafquen
        DB_HOST=postgres
        DB_PORT=5432
        DB_NAME=e1_ass

        HOST=broker.legit.capital
        USER=students
        PORT=9000
        PASSWORD=iic2173-2023-2-students
        GROUP_ID=13

-   Correr docker-compose build y docker-compose up
-	Correr el mqtt con python mqtt.py
-	Correr la API con python app/main.py



**Frontend:**

-	Clonar repositorio https://github.com/conicorreag/E1_Frontend_Grupo13_Arqui 
-	En el terminal, correr npm install para asegurarse de tener todas las dependencias necesarias.
-	Crear un .env con las credenciales:

        REACT_APP_BACKEND_URL = "http://0.0.0.0:8000"

-   En caso de que haya algun problema con el .env, exportar en la terminal REACT_APP_BACKEND_URL = http://0.0.0.0:8000
-	Correr npm run start para comenzar.