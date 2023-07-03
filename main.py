### AQUI ES DONDE VAMOS A DESARROLLAR EL CODIGO NECESARIO PARA PODER LEVANTAR UN SERVIDOR WEB API Y CREAR NUESTRO ENDPOINT

from fastapi import FastAPI

app = FastAPI() # Lo instanciamos. Esta variable nos va a permitir correr un proyecto

@app.get(path="/") # Se llama "path operation decorator". Es un decorador para una función a crear. Utiliza el objeto get que viene del obj app.
def index():
    return {"message":"Mira Shaila!!!!! MI PRIMER API!!!!"}

# Lo que acabamos de hacer es que cada vez que se consulte a la ruta "/"(o la ruta por defecto) se va a
# ejecutar la funcion index

# luego desde la terminal iniciaremos la API. Esto lo haremos con UVICORN.
# Ejecutaremos "uvicorn main:app --reload" ------> "main" por el nombre del archivo. "app" que es el objeto de nuestra aplicación,
# "--reload" es un modificador que nos permitira realizar cambios en el codigo sin tener que levantar el servidor nuevamente, sino
# que lo detecta y lo vuelve a correr automáticamente.

# EN BASE A ESTO UVICORN VA A ESTAR CORRIENDO POR DEFECTO EN EL LOCALHOST/PUERTO 8000
