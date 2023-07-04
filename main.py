import uvicorn
from fastapi import FastAPI

# Como vamos a trabajar con modelos de datos usando Pydantic y estamos usando un servicio web que nos
# retorna un archivo JSON formateado, necesitamos algunos utilitarios de FastAPI para poder transformar
# las instancias de las clases con Pydantic a un diccionario JSON y poder retornarlos sin problemas. Para 
# esto vamos a importa las siguientes librerias:

from fastapi.encoders import jsonable_encoder # transforma la instancia que tenemos con el modelo de datos a un diccionario JSON
from fastapi.responses import JSONResponse # formatea la respuesta JSON y poder incluir el código de estado en la API

from pydantic import BaseModel # BaseModel nos servirá para poder crear las Clases/modelos de datos. 
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
async def get_all_tools(): # funcion asincronica como parte de la sincronia que caracteriza a starlet y FastAPI que nos retornara toda la tool_list
    return JSONResponse(content= tools_list, status_code= 200) # devolvemos la rta. y el código de estado.

####
# hacemos una prueba con el comando uvicorn main:app --reload
