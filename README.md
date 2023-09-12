# 2023-2 / IIC2173 - E0 | Fintech Async


## Consideraciones generales
- Se logró todo lo pedido. La parte variable elegida fue HTTPS. 
- La paginacion predeterminada es pag=1 y size=30 (si no se especifica una)
- El nginx.conf esta en la carpeta config
- Para hacer la entrega me ayudé de ChatGPT, Copilot y la documentacion de FastAPI.


## Nombre del dominio
arquiconicorrea.me


## Links

- Para ver stocks: https://arquiconicorrea.me/stocks
- Para ver detalle historico de un stock (por ejemplo AMZN): https://arquiconicorrea.me/stocks/AMZN
- Para paginar (por ejemplo pagina 2, tamaño 25): https://arquiconicorrea.me/stocks/AMZN?page=2&size=25


## IP de la instancia (elastica)
3.19.204.166


## Método de acceso al servidor con archivo .pem y ssh
Abrir terminal en carpeta donde esten las llaves y correr:

ssh -i "Claves_E0_ASS.pem" ubuntu@ec2-3-19-204-166.us-east-2.compute.amazonaws.com

En mi computador no era necesario poner 'sudo' al principio, pero puede ser necesario en otros. 


## Puntos logrados o no logrados
Se logró todo






