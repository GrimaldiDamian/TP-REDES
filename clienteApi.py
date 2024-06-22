import requests
import json
from clases import *

url = "http://localhost:8000"

def verArchivo():
    respuesta = requests.get(f'{url}/Leer_Archivo')
    respuesta.raise_for_status()
    return respuesta.json()

def VerCategorias():
    respuesta = requests.get(f'{url}/Categorias')
    return respuesta.json()

def BuscarPremio():
    anio = int(input("Ingrese un anio: "))
    categoria = input("Ingrese una categoria: ")
    respuesta = requests.get(f'{url}/Buscar_Premio', params={"year":str(anio),"category":categoria})
    respuesta.raise_for_status()
    return respuesta.json()

def AgregarPremio():
    pass

def ActualizarLaureate():
    pass

def ActualizarCategoria():
    pass

def EliminarPremio():
    pass

def menu():
    while True:
        op = int(input("1)Ver archivo json\n2)Ver categorias\n3)Buscar premio\n4)Agregar premio\n5)Actualizar laureate\n6)Actualizar categoria\n7)Eliminar Premio\n0)Salir\nIngrese la opcion que deseas realizar: "))
        if op == 0:
            break
        elif op==1:
            print(verArchivo())
        elif op ==2:
            print(VerCategorias())
        elif op == 3:
            print(BuscarPremio())
        elif op == 4:
            print(AgregarPremio())
        elif op==5:
            print(ActualizarLaureate())
        elif op==6:
            print(ActualizarCategoria())
        elif op==7:
            print(EliminarPremio())

menu()