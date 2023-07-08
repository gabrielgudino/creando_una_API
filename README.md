# Tools API

En este proyecto se quiere hacer un sistema de recomendación de herramientas informáticas según sea el perfil del usuario.
Para ello, se debe poblar una BB.DD. con herramientas informáticas de toda índole (software, data, cloud, etc.).
De esta manera, se harán operaciones de lectura, creación, actualización y borrado en la BB.DD. Para ello, se solicita la 
implementación de un API que pueda hacer dichas operaciones.

Para poder cumplir este proyecto hicimos un CRUD mediante un API. Para ésto, utilizamos FastAPI mediante sus
métodos GET, POST, PUT y DELETE. Un vez terminado se desplegó en Deta Space.

## Requerimiento
Luego de crear la primer instancia (4to commit) nos solicitan añadir la categoría en el endpoint que obtiene todas las 
herramientas, de manera que si se envía, filtra los resultados y obtiene las herramientas de dicha categoría. En caso 
contrario muestra todas.

## Deta Space Hosting
Aquí es donde realizaremos el despliegue donde se hosteará nuestra aplicación, permitiendo levantar nuestro proyecto en sus 
servidores y brindar una URL pública para poder acceder. En primer instancia debemos hacernos de un usuario y luego instalar 
el cliente (atento con la llave!). Una vez instalado el cliente ejecutamos en nuestra linea de comando (CMD ya que esto se probó en win): 

iwr https://get.deta.dev/space-cli.ps1 -useb | iex 

space login (donde ingresaremos la key que creamos)

Una vez realizado esto, en nuestro proyecto deberemos modificar el "requirements.txt" ya que no utilizaremos uviconr (lo borramos), 
puesto que Deta Space levanta el server por si mismo. Además no necesitaremos todos los utilitarios de fastapi asi que le borraremos el "[all]". 
Tampoco olvidarse de comentar el "import". Ahora, para desplegar la API, dentro de la carpeta del proyecto desde el CMD tipeamos: 

space new 

Y aceptamos el kernel que nos sugiere. Luego ejecutamos: 

space push 

Una vez pusheado nos dará una dirección para acceder, si le agregamos a esta "/docs" nos permitirá acceder al entorno gráfico de FastAPI. 
¡¡¡ Ya tenemos desplegado el proyecto en una URL pública !!! (Lamentablemente Deta Space solo permite acceder con credenciales ya que está dentro de su entorno).