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


