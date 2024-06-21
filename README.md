Ejecutar el siguiente codigo:

git clone https://github.com/DamianGrimaldi/TP-REDES.git

Luego en la carpeta creada, si estas desde windows, se debera ejecutar los siguientes comandos (sin los comentarios #):

python -m venv ./.venv #para crear un entorno virtual
.venv\Scripts\activate  #para activarlo

Una vez hecho, deberas descargar las librerias necesarias:

pip install fastapi
pip install requests
pip install uvicorn

A la hora de ejecutar el archivo main (servidor api)
utilizar el siguiente comando:

uvicorn main:app --host 0.0.0.0 --reload
el host sirve para que cualquier dispositivo de la misma red se pueda conectarse, y para hacerlo, tiene que ser la misma direccion ip
para ver cual es la direcciones ip, desde windows, se tiene que ejecutar ipconfig, y buscar una que diga 192.168.x.x (x, es cualquier numero) y a continuacion el numero del puerto.

Luego con una pagina web ingresar:

http://127.0.0.1:8000/docs #En la parte de los numeros seria, con lo que sale luego de uvicorn, y en la parte de docs, para ir probando los metodos.