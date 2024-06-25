from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt
from clases import *
import json

app = FastAPI()
contraseña = OAuth2PasswordBearer(tokenUrl="token") #token tiene que estar creada

secret_key = "Prueba de contraseña"

users = {
    "administrador" : {"username": "administrador","email":"administrador@gmail.com","password":"4321", "tipo de usuario": "admin"},
    "user2" :  {"username": "user2","email":"user2@gmail.com","password":"1234","tipo de usuario": "cliente"}
}

def encode_token(payload:dict) ->str:
    token = jwt.encode(payload, secret_key,algorithm="HS256")
    return token

def decode_token(token:Annotated[str,Depends(contraseña)]) -> dict:
    data = jwt.decode(token,secret_key,algorithms=["HS256"])
    user = users.get(data["username"])
    return user

@app.post("/token")
def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Usuario o password incorrecto")
    
    token = encode_token({"username": user["username"],"email":user["email"]})
    return {"access_token":token}

def cargar_archivo():
    with open("prize.json", 'r', encoding='utf-8') as file:
        dicJson = json.load(file)
    return dicJson

archivo = cargar_archivo()

def actualizarArchivo():
    try:
        with open("prize.json", "w") as file:
            json.dump(archivo, file, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando el archivo JSON: {e}")

@app.get("/Leer_Archivo")

def Leer_Archivo(user:Annotated[dict,Depends(decode_token)]):
    if not user:
        return archivo

@app.get("/Categorias")

def Categorias(user:Annotated[dict,Depends(decode_token)]):
    categorias = []
    for valores in archivo.get("prizes", []):
        if valores.get("category") not in categorias:
            categorias.append(valores["category"])
    
    return categorias
    
@app.get("/Buscar_Premio")

def Buscar_Premio(user:Annotated[dict,Depends(decode_token)],year:str,category:str):
    lista = []
    year_found = False
    category_found = False
    
    for premios in archivo.get("prizes", []):
        if premios.get("year") == year:
            year_found = True
            if premios.get("category") == category:
                category_found = True
                for participantes in premios.get("laureates", []):
                    nombre_completo = f"{participantes['firstname']} {participantes['surname']}"
                    motivacion = participantes.get("motivation", "Motivación no especificada")
                    datos_participante = f"Nombre del participante: {nombre_completo}, su motivación: {motivacion}"
                    lista.append(datos_participante)
    
    if not year_found:
        raise HTTPException(status_code=404, detail=f"Error: El año {year} no se encontró en el archivo.")
    if not category_found:
        raise HTTPException(status_code=404, detail=f"Error: La categoría {category} no se encontró para el año {year}.")
    
    return lista

@app.post("/Agregar_Premio")

def Agregar_Premio(user: Annotated[dict,Depends(decode_token)],Premiados : dict):
    
    if user["tipo de usuario"] == "admin":
    
        if Premiados not in archivo["prizes"]:
            total = len(Premiados["laureates"])

            if total != int(Premiados["laureates"][0]["share"]):
                raise HTTPException(status_code=404, detail=f"La cantidad de shares no coincide con la cantidad de laureados. {len(Premiados["laureates"])}, {int(Premiados["laureates"][0]["share"])}")

            archivo["prizes"].append(Premiados)
            archivo["prizes"] = sorted(archivo["prizes"], key=lambda x: x["year"], reverse=True)
            actualizarArchivo()
        else:
            raise HTTPException(status_code=400, detail="Ya existe dicho premio")
        return {"nuevo_premio": Premiados, "mensaje": "Se guardó correctamente"}
    
    else:
        raise HTTPException(status_code=403, detail="Fue rechazado por el servidor")

@app.put("/Actualizar_Laureate")

def Actualizar_Laureate(user: Annotated[dict,Depends(decode_token)],premioNuevo: dict):
    
    if user["tipo de usuario"] == "admin":
    
        for premio in archivo.get("prizes", []):
            if premio["year"] == premioNuevo["year"] and premio["category"] == premioNuevo["category"]:
                laureateAnterior = premio["laureates"]
                premio["laureates"] = premioNuevo["laureates"]
                actualizarArchivo()
                return f"El laureado: {laureateAnterior} fue cambiado a {premioNuevo["laureates"]}"
        
        raise HTTPException(status_code=404, detail="Fecha o categoría no encontrada")
    
    else:
        return f"Permiso denegado"

@app.put("/Actualizar_Categoria")

def Actualizar_Categoria(user: Annotated[dict,Depends(decode_token)], year:int,categoria_Anterior:str,categoria_Nueva:str):
    
    if user["tipo de usuario"] == "admin":
    
        year = str(year)
        for premio in archivo.get("prizes",[]):
            if premio["year"] == year and premio["category"] == categoria_Anterior:
                premio["category"] = categoria_Nueva
                actualizarArchivo()
                return f"La nueva categoria fue exitosa"
        
        raise HTTPException(status_code=404, detail="Error en el año o en la categoría ingresada")
    
    else:
        return f"Permiso denegado"

@app.delete("/Eliminar_Premio")

def Eliminar_Premio(user: Annotated[dict,Depends(decode_token)], Premiados:dict):
    
    if user["tipo de usuario"] == "admin":
        
        if Premiados in archivo["prizes"]:
            archivo["prizes"].remove(Premiados)
            actualizarArchivo()
            return f"El premio se ha eliminado"
        else:
            raise HTTPException(status_code=404, detail="No se pudo eliminar, porque el premio no existe")
    
    else:
        return f"Permiso denegado"