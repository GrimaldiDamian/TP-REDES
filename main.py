from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

class Laureate(BaseModel):
    id: int
    firstname: str
    surname: str
    motivation: str
    share: int
    def convertirDict(self):
        return {
            "id": str(self.id),
            "firstname": self.firstname,
            "surname": self.surname,
            "motivation": self.motivation,
            "share": str(self.share)
        }

class Premio(BaseModel):
    anio:int
    categoria:str
    laureate : list[Laureate]
    overallMotivation : Optional[str] = None
    def convertirDict(self):
        if self.overallMotivation != None:
            return {
                "year": str(self.anio),
                "category": self.categoria,
                "laureates": [laureate.convertirDict() for laureate in self.laureate],
                "overallMotivation": self.overallMotivation
            }
        else:
            return {
                "year": str(self.anio),
                "category": self.categoria,
                "laureates": [laureate.convertirDict() for laureate in self.laureate],
            }

def archivo():
    with open("prize.json", 'r') as file:
        dicJson = json.load(file)
    return dicJson

archivo = archivo()

def actualizarArchivo():
    with open("prize.json", "w") as file:
        json.dump(archivo, file)

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
        return f"Error: El año {year} no se encontró en el archivo."
    if not category_found:
        return f"Error: La categoría {category} no se encontró para el año {year}."
    
    return lista

@app.post("/Agregar_Premio")

def Agregar_Premio(Premiados : Premio):
    
    nuevo_premio = Premiados.convertirDict()
    
    archivo["prizes"].append(nuevo_premio)
    archivo["prizes"] = sorted(archivo["prizes"], key=lambda x: x["year"], reverse=True)
    
    with open("prize.json","w") as file:
        json.dump(archivo,file)
    
    return nuevo_premio, f"Se guardo correctamente"

@app.put("/Actualizar_Laurete")

def Actualizar_Laurete(year: int, categoria: str, laureates: list[Laureate]):
    for premio in archivo.get("prizes", []):
        if premio["year"] == str(year) and premio["category"] == categoria:
            laureateAnterior = premio["laureates"]
            laureateActual = [laureate.convertirDict() for laureate in laureates]
            premio["laureates"] = laureateActual
            actualizarArchivo()
            return f"El laureado: {laureateAnterior} fue cambiado a {laureateActual}"
    
    return "Fecha o categoría no encontrada"

@app.put("/Actualizar_Categoria")

def Actualizar_Categoria(year:int,categoria_Anterior:str,categoria_Nueva:str):
    year = str(year)
    for premio in archivo.get("prizes",[]):
        if premio["year"] == year and premio["category"] == categoria_Anterior:
            premio["category"] = categoria_Nueva
            actualizarArchivo()
            return f"La nueva categoria fue exitosa"
    
    return f"Error en el año o en la categoria ingresada"

@app.delete("/EliminarPremio")

def EliminarPremio(premio:Premio):
    premio = premio.convertirDict()
    if premio in archivo["prizes"]:
        archivo["prizes"].remove(premio)
        actualizarArchivo()
        return f"El premio se ha eliminado"
    else:
        return f"No se pudo eliminar, porque el premio no existe"