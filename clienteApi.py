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
    categoria = input("Ingrese una categoria: ").lower()
    respuesta = requests.get(f'{url}/Buscar_Premio', params={"year":str(anio),"category":categoria})
    respuesta.raise_for_status()
    return respuesta.json()

def agregarLaureate():
    lista =[]
    
    share = int(input("Ingrese con cuantos participantes se comparte: "))
    for i in range(share):
        id = int(input("Ingrese el id: "))
        firstname = input("Ingrese el nombre del laureado: ")
        surname = input("Ingrese el apellido del laureado: ")
        motivation = input("Ingrese la motivación del laureado: ")
        laureates = Laureate(id=id, firstname=firstname, surname=surname, motivation=motivation, share=share)
        lista.append(laureates)
    
    return lista

def AgregarPremio():
    year = int(input("Ingrese el anio del premio: "))
    
    categoria = input("Ingrese la categoria: ")
    
    overallMotivation = input("Si hay overallMotivation, ingreselo o saltea (ingrese None para saltear) ")
    overallMotivation = overallMotivation if overallMotivation != "None" else None
    
    laureate = agregarLaureate()
    
    premio = Premio(anio=year, categoria=categoria, laureate=laureate, overallMotivation=overallMotivation)
    premio_dict = premio.convertirDict()
    
    respuesta = requests.post(f"{url}/Agregar_Premio", json = premio_dict)
    respuesta.raise_for_status()
    return respuesta.json()

def ActualizarLaureate():
    year = int(input("Ingrese el anio del premio que quieres modificar: "))
    categoria = input("Ingrese la categoria que quieres modificar: ")
    laureate = agregarLaureate()
    
    premio = Premio(anio=year, categoria=categoria, laureate=laureate, overallMotivation=None)
    premio_dict = premio.convertirDict
    
    respuesta = requests.post(f"{url}/Actualizar_Laureate", json = premio_dict)
    respuesta.raise_for_status()
    return respuesta.json()

def ActualizarCategoria():
    year = int(input("Ingrese el anio del premio que quieres modificar: "))
    categoria = input("Ingrese la categoria que quieres modificar: ")
    categoriaNueva = input("Ingrese la nueva categoria: ")
    
    respuesta = requests.post(f"{url}/Actualizar_Laureate", params={"year": year, "categoria_Anterior": categoria, "categoria_Nueva": categoriaNueva})
    respuesta.raise_for_status()
    return respuesta.json()

def EliminarPremio():
    year = int(input("Ingrese el anio del premio que deseas eliminar: "))
    
    categoria = input("Ingrese la categoria que deseas eliminar:  ")
    
    overallMotivation = input("Si hay overallMotivation, ingreselo o saltea (ingrese None para saltear) ")
    overallMotivation = overallMotivation if overallMotivation != "None" else None
    
    laureate = agregarLaureate()
    
    premio = Premio(anio=year, categoria=categoria, laureate=laureate, overallMotivation=overallMotivation)
    premio_dict = premio.convertirDict()
    
    respuesta = requests.delete(f"{url}/Eliminar_Premio", json = premio_dict)
    respuesta.raise_for_status()
    return respuesta.json()

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