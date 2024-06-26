Ejecutar el siguiente codigo:

git clone https://github.com/DamianGrimaldi/TP-REDES.git

Ejecutar el siguiente comando dependiendo del sistema operativo

PARA WINDOWS:

python -m venv ./.venv #para crear un entorno virtual
.venv\Scripts\activate  #para activarlo

PARA LINUX:
python3 -m venv ./venv #para crear un entorno virtual
source ./.venv/bin/activate # para activarlo

Una vez hecho, deberas descargar las librerias necesarias:

pip install fastapi         #creacion de apis
pip install requests        #abrir url
pip install uvicorn         #ejecucion de servidor apo
pip install python-jose     #Para generar las claves
pip install pydantic        #Para crear un modelo de datos para uso de las clases

A la hora de ejecutar el archivo main (servidor api)
utilizar el siguiente comando:

uvicorn main:app --host 0.0.0.0 --reload # se puede omitir --reload, ya que esta porcion de comando, ya que le dice a Uvicorn que vuelva a cargar el servidor cuando detecta cambios.

El host sirve para que cualquier dispositivo de la misma red se pueda conectar.

Luego con una pagina web ingresar:

http://localhost:8000/docs     #Acceso al servidor, para ver el contenido

Una vez realizado hasta este punto, para que haya una comunicacion entre cliente-servidor se tendria que ejecutar primero la api, para que se mantenga encendida a la hora de ejecutar el archivo de clienteApi. 
Despues se ejecuta el archivo clienteApi.py
