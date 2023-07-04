# Tools API

En este proyecto se quiere hacer un sistema de recomendación de herramientas informáticas según sea el perfil del usuario.
Para ello, se debe poblar una BB.DD. con herramientas informáticas de toda índole (software, data, cloud, etc.).
De esta manera, se harán operaciones de lectura, creación, actualización y borrado en la BB.DD. Para ello, se solicita la 
implementación de un API que pueda hacer dichas operaciones.

Para poder cumplir este proyecto hacimos un CRUD mediante un API. Para ésto, utilizamos FastAPI mediante sus
métodos GET, POST, PUT y DELETE. Un vez terminado se desplegó en Deta Space.

## Requerimiento
Luego de crear la primer instancia (4to commit) nos solicitan añadir la categoría en el endpoint que obtiene todas las 
herramientas, de manera que si se envía, filtra los resultados y obtiene las herramientas de dicha categoría. En caso 
contrario muestra todas.