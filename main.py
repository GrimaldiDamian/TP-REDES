from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt
import json

app = FastAPI()
contraseña = OAuth2PasswordBearer(tokenUrl="token") #token tiene que estar creada

secret_key = "Prueba de contraseña"

users = {
    "damian" : {"username": "damian","email":"grimaldidamian001@gmail.com","password":"1234"},
    "user2" :  {"username": "user2","email":"user2@gmail.com","password":"1234"}
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
    try:
        with open("prize.json", 'r') as file:
            dicJson = json.load(file)
        return dicJson
    except FileNotFoundError:
        return {"prizes": []}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error leyendo el archivo JSON")

archivo = cargar_archivo()

def actualizarArchivo():
    try:
        with open("prize.json", "w") as file:
            json.dump(archivo, file, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando el archivo JSON: {e}")

@app.get("/Leer_Archivo")

def Leer_Archivo():
    return archivo

@app.get("/Categorias")

def Categorias():
    categorias = []
    for valores in archivo.get("prizes", []):
        if valores.get("category") not in categorias:
            categorias.append(valores["category"])
    
    return categorias

@app.get("/Buscar_Premio")

def Buscar_Premio(year:str,category:str):
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

def Agregar_Premio(Premiados : Annotated[dict,Depends(decode_token)]):
    if Premiados not in archivo["prizes"]:
        total = len(Premiados["laureates"])

        if len(Premiados["laureates"]) != int(Premiados["laureates"][0]["share"]):
            raise HTTPException(status_code=404, detail=f"La cantidad de shares no coincide con la cantidad de laureados. {len(Premiados["laureates"])}, {int(Premiados["laureates"][0]["share"])}")

        archivo["prizes"].append(Premiados)
        archivo["prizes"] = sorted(archivo["prizes"], key=lambda x: x["year"], reverse=True)
        actualizarArchivo()
    else:
        raise HTTPException(status_code=400, detail="Ya existe dicho premio")
    return {"nuevo_premio": Premiados, "mensaje": "Se guardó correctamente"}

@app.put("/Actualizar_Laureate")

def Actualizar_Laurete(premioNuevo: Annotated[dict,Depends(decode_token)]):
    for premio in archivo.get("prizes", []):
        if premio["year"] == premioNuevo["year"] and premio["category"] == premioNuevo["category"]:
            laureateAnterior = premio["laureates"]
            premio["laureates"] = premioNuevo["laureates"]
            actualizarArchivo()
            return f"El laureado: {laureateAnterior} fue cambiado a {premioNuevo["laureates"]}"
    
    raise HTTPException(status_code=404, detail="Fecha o categoría no encontrada")

@app.put("/Actualizar_Categoria")

def Actualizar_Categoria(year:Annotated[int,Depends(decode_token)],categoria_Anterior:Annotated[str,Depends(decode_token)],categoria_Nueva:Annotated[str,Depends(decode_token)]):
    year = str(year)
    for premio in archivo.get("prizes",[]):
        if premio["year"] == year and premio["category"] == categoria_Anterior:
            premio["category"] = categoria_Nueva
            actualizarArchivo()
            return f"La nueva categoria fue exitosa"
    
    raise HTTPException(status_code=404, detail="Error en el año o en la categoría ingresada")

@app.delete("/Eliminar_Premio")

def Eliminar_Premio(Premiados:Annotated[dict,Depends(decode_token)]):
    if Premiados in archivo["prizes"]:
        archivo["prizes"].remove(Premiados)
        actualizarArchivo()
        return f"El premio se ha eliminado"
    else:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, porque el premio no existe")