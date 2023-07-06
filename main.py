import uvicorn
from fastapi import FastAPI

# Como vamos a trabajar con modelos de datos usando Pydantic y estamos usando un servicio web que nos
# retorna un archivo JSON formateado, necesitamos algunos utilitarios de FastAPI para poder transformar
# las instancias de las clases con Pydantic a un diccionario JSON y poder retornarlos sin problemas. Para 
# esto vamos a importa las siguientes librerias:

from fastapi.encoders import jsonable_encoder # transforma la instancia que tenemos con el modelo de datos a un diccionario JSON
from fastapi.responses import JSONResponse # formatea la respuesta JSON y poder incluir el código de estado en la API

from pydantic import BaseModel # BaseModel nos servirá para poder crear las Clases/modelos de datos. 
from typing import Union # nos permite definir parámetros tipo query opcionales en nuestra API
# from typing import Optional # lo utilizamos si en el modelo de datos vamos a tener variables opcionales.

from constants import FAKE_DB_TOOLS # ver ## 2

tools_list = list()
tools_list.extend(FAKE_DB_TOOLS)

# Creamos la clase que va a instanciar BaseModel

class Tool(BaseModel):
    id: str
    name: str
    category: str
#   email: Optional[str] # ejemplo de como crear una variable opcional

## 2
# Definido el modelo de datos Tool(BaseModel) no tenemos que olvidar de importar la variable que definimos en constants.py siendo la data inicial
# la que tenemos allí pero que estará sujeta a lectura, inserciones y modificaciones/eliminaciones. Es por esto que tenemos que tener una 
# lista auxiliar que nos permita guardar la data hasta el momento que sea necesario. Para ello es que importamos FAKE_DB_TOOLS que será agregada 
# a nuestra lista auxiliar.

####
# En este punto ya estamos listos para crear nuestro primer endpoint que nos va a retornar todas las herramientas de la BB.DD. creada
# hasta el momento. Para ello vamos a definir la variable que va a almacenar toda nuestra aplicación:

app = FastAPI() # instancia de FastAPI()

# luego debemos indicarle a nuestro servidor cual va a ser la ruta que nos va a devolver todas las herramientas:

@app.get(path="/api/tools/get_all") # esto indica el metodo http.
async def get_all_tools(category: Union[str, None] = None): # el framework los parametros tipo query se insertan como argumentos de la función(FastAPI los detecta y recupera)
    response = tools_list # al ser la respuesta por defecto "None", nos va a devolver la tool_list completa
    if category: # nos vamos a asegurar que la categoría exista con este "if". Si existe sigue
        response = list(filter(lambda x: x["category"] == category, tools_list))  # NOTA 1
    return JSONResponse(content= tools_list, status_code= 200) # devolvemos response según haya sido el requerimiento/query y el código de estado.

####
# hacemos una prueba con el comando uvicorn main:app --reload
# NOTA 1: Lo que hace aca es devolver una lista que recibe como parámetro un filtro que a su vez recibe como parámetro una función lambda 
# que recibe la lista a filtrar. Ademas agregamos como parámetro la lista a filtrar.

# 7mo commit - "Path Params"
@app.get(path='/api/tools/{tool_id}') # NOTA 2
async def get_tool(tool_id: str):
    response = None
    status_code = 404

    for tool in tools_list:
        if tool['id'] == tool_id:
            response = tool
            status_code = 200
            break
    return JSONResponse(content=response, status_code=status_code)

# NOTA 2: Al acceder a localhost:8000/docs veremos que en la documentación tenemos un nuevo "endpoint", el cual es el que obtiene una herramienta
# en base al "id". Al probar este "endppoint", si mandamos un "id" que figura en nuestro archivo nos devolverá el mismo, caso contrario nos devolverá 
# un Null con el código 404.