from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Laureate(BaseModel):
    id: int
    firstname: str
    surname: str
    motivation: str
    share: int

def archivo():
    with open("prize.json", 'r') as file:
        dicJson = json.load(file)
    return dicJson

archivo = archivo()

@app.get("/LeerArchivo")

def LeerArchivo():
    return archivo

@app.get("/Categorias")

def Categorias():
    categorias = []
    for valores in archivo.get("prizes", []):
        if valores.get("category") not in categorias:
            categorias.append(valores["category"])
    
    return categorias

@app.get("/BuscarPremio")

def BuscarPremio(year:str,category:str):
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
        return f"Error: El año {year} no se encontró en el archivo."
    if not category_found:
        return f"Error: La categoría {category} no se encontró para el año {year}."
    
    return lista

@app.post("/agregarPremio")

def agregarPremio(anio:int,categoria:str,Premiados:list[Laureate]):
    laureates_dict = []
    for premiado in Premiados:
        premiado_dict = {
            "id": str(premiado.id),
            "firstname": premiado.firstname,
            "surname": premiado.surname,
            "motivation": premiado.motivation,
            "share": str(premiado.share)
        }
        laureates_dict.append(premiado_dict)
    nuevo_premio = {
        "year": str(anio),
        "category": categoria,
        "laureates": laureates_dict
    }
    
    archivo["prizes"].append(nuevo_premio)
    archivo["prizes"] = sorted(archivo["prizes"], key=lambda x: x["year"], reverse=True)
    
    with open("prize.json","w") as file:
        json.dump(archivo,file)
    
    return nuevo_premio