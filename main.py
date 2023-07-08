import uvicorn
from fastapi import FastAPI

# Como vamos a trabajar con modelos de datos usando Pydantic y estamos usando un servicio web que nos
# retorna un archivo JSON formateado, necesitamos algunos utilitarios de FastAPI para poder transformar
# las instancias de las clases con Pydantic a un diccionario JSON y poder retornarlos sin problemas. Para 
# esto vamos a importa las siguientes librerias:

from fastapi.encoders import jsonable_encoder # transforma la instancia que tenemos con el modelo de datos a un diccionario JSON
from fastapi.responses import JSONResponse # formatea la respuesta JSON y poder incluir el código de estado en la API

from pydantic import BaseModel # BaseModel nos servirá para poder crear las Clases/modelos de datos. 
from typing import Union, Optional # nos permite definir parámetros tipo query opcionales en nuestra API
# from typing import Optional # lo utilizamos si en el modelo de datos vamos a tener variables opcionales. Lo agregamos junto con Union en la linea
# anterior.

from constants import FAKE_DB_TOOLS # ver ## 2

tools_list = list()
tools_list.extend(FAKE_DB_TOOLS)

# Creamos la clase que va a instanciar BaseModel

class Tool(BaseModel):
    id: Optional[str] = None # None es por defecto. Lo pusimos opcional por el método PUT.
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

@app.get(path="/api/tools/get_all") # esto indica el metodo http. "endpoint1"
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
@app.get(path='/api/tools/{tool_id}') # NOTA 2 "endopoint2"
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

# 8vo commit - "Método Post"
# Este método es utilizado para crear nuevos registros en el API. Implementaremos un nuevo endpoint del tipo POST, el cual va a recibir en el
# "request body" el objeto a crear en el listado. Para ésto es necesario crear un modelo de datos. Ésto ya lo hicimos al crear la clase "Tool" en la
# linea 23 que hereda de la base BaseModel. Los atributos son "id", "name", "category". El objeto se recibirá como JSON en la API y FastAPI se encargará
# de parsearlo y convertirlo en una clase con su modelo de datos. Como el modelo este se utlizará tanto para el metodo POST, como el PUT se necesitara
# que el atributo id sea opcional.
@app.post(path='/api/tools') # NOTA 3 Los parámetros del tipo "request body" no son parte del endpoint, x lo que se va a enviar como tales ("request body") 
# de la sig. manera:
async def create_tool(tool:Tool): # Lo q hace FastAPI es leer el "request body", obtener los atributos necesarios para instanciar la clase Tool devolviendo una instancia de la misma.
    tool_id = tool.id # si este id existe queda como tal, sino existe debemos hacer una generación.
    if tool_id is not None: # validamos si existe o no tool_id
        tool.id = f'{tool.name}-{tool.category}' # si no existe creamos el id
    tools_list.append(tool.dict()) # lo agregamos a constants.py
    json_data = jsonable_encoder(tool)
    return JSONResponse(content=json_data, status_code=201)

# 9no commit - "Método PUT"
# Este método lo utilizaremos para reemplazar o actualizar un registro en nuestra API. Para ello tenemos que recibir 2 párametros, el id a buscar a efectos de
# que si lo encuentra actualiza el "Documento". También tenemos que recibir el objeto que queremos reemplazar de esta base de datos. De esta manera crearemos
# un endpoint que reciba un "path parameter" para el "id" y un "request body" para el objeto que queremos actualizar.
# LA FUNCIÓN find_index_by_id() DEBIERA ESTAR EN LA CABEZA DEL SCRIPT POR CUESTIONES DE PROLIJIDAD, PERO LA DEJAREMOS AQUI POR CUESTIONES DIDÁCTICAS.
def find_index_by_id(tool_id): # el argumento es el "id" de la herramienta a buscar.
    _index = None # por defecto tiene un valor nulo que retornará si no encuentra el "id".
    for index, value in enumerate(tools_list): #enumerate() nos convierte la lista en constants.py en un objeto JSON.
        if value['id'] == tool_id:
            _index = index # guarda como clave el índice 
            break
    return _index

# Este endpoint es invocado por el método http "put", el cual va a recibir 2 parámetros. El primero será un "path parameter" el cual guardará el "id" de la 
# herramienta a actualizar (si esta existe la actualizamos, sino retornamos un código 404).  El segundo será un "request body" el objeto que queremos reemplazar.
# Para poder hacer todo ésto necesitaremos encontrar el índice de la lista del "id" que queremos actualizar. Es por ésto que se creo la función find_index_by_id().
@app.put(path='/api/tools/{tool_id}') # Método PUT con su ruta y su parámetro de path
async def update_tool(tool_id: str, tool: Tool): # La función asincrónica se encargará de actualizar el "id". Recibe 2 parámetros, el "id" y el objeto Tool como "request body".
    if tool.id is None: # aquí aplicamos una lógica similar al método POST. Validamos que el tool_id sea nulo para poder generarlo.
        tool.id = f'{tool.name}-{tool.category}' # Al ser nulo generamos el "id" concatenando el nombre y la categoría en tool.
    index_update = find_index_by_id(tool_id=tool_id) # Una vez listo el elemento para actualizar buscamos el elemento en la lista guardandolo en "index_update"
    if index_update is None: # si la busqueda de indice es nula tenemos que retornar None y un 404. 
        return JSONResponse(content=None, status_code=404)
    else: # aca si ha sido encontrado el index. Entonces reemplazamos el elemento.
        tools_list[index_update] = tool.dict() # lo actualizamos con el objeto tool que indicamos como argumento en update_tool()
    return JSONResponse(content=True, status_code=200)