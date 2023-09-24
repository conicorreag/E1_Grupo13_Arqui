# Diagrama de componentes
## Frontend
En el diagrama se puede apreciar dentro del frontend el componente **REACTAPP** que  es una aplicacion en react, esta aplicacion esta conformada por componentes y porlotanto depende de ellos para su funcionamiento.
Los Archivos de reactAPP estan alojados en S3 y mediante cloudfront el usuario puede acceder al frontend.
A su vez para la autentificacion de usuario el frontend ocupa auth0 de forma externa.

## Backend
Cuando se realiza algun request desde react APP hasta el backend, este se realiza mediante la api Gateway que ademas de realizar autentificacion, redirecciona hacia una instancia EC2 donde se encuentra Fastapi que maneja el backend.

Fastapi tiene un modulo mqtt que se encarga de escuchar las validaciones y stocks recibidas desde el broker. Fastapi tambien es la encargada de hacer las publish de las solicitudes de compra y manejar la base de datos stocks.

![Alt text](image-1.png)