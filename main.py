from fastapi import FastAPI
import json

app = FastAPI()

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