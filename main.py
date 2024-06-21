from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import json
import datetime

app = FastAPI()

class Laureate(BaseModel):
    id: int
    firstname: str
    surname: str
    motivation: str
    share: int = Field(ge=1)
    def convertirDict(self):
        return {
            "id": str(self.id),
            "firstname": self.firstname,
            "surname": self.surname,
            "motivation": self.motivation,
            "share": str(self.share)
        }

class Premio(BaseModel):
    anio:int = Field(le = datetime.date.today().year, ge=1901)
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

def Agregar_Premio(Premiados : Premio):
    nuevo_premio = Premiados.convertirDict()

    if nuevo_premio not in archivo["prizes"]:
        total = len(nuevo_premio["laureates"])

        if len(nuevo_premio["laureates"]) != int(nuevo_premio["laureates"][0]["share"]):
            raise HTTPException(status_code=404, detail=f"La cantidad de shares no coincide con la cantidad de laureados. {len(nuevo_premio["laureates"])}, {int(nuevo_premio["laureates"][0]["share"])}")

        archivo["prizes"].append(nuevo_premio)
        archivo["prizes"] = sorted(archivo["prizes"], key=lambda x: x["year"], reverse=True)
        actualizarArchivo()
    else:
        raise HTTPException(status_code=400, detail="Ya existe dicho premio")
    return {"nuevo_premio": nuevo_premio, "mensaje": "Se guardó correctamente"}

@app.put("/Actualizar_Laureate")

def Actualizar_Laurete(year: int, categoria: str, laureates: list[Laureate]):
    for premio in archivo.get("prizes", []):
        if premio["year"] == str(year) and premio["category"] == categoria:
            laureateAnterior = premio["laureates"]
            laureateActual = [laureate.convertirDict() for laureate in laureates]
            premio["laureates"] = laureateActual
            actualizarArchivo()
            return f"El laureado: {laureateAnterior} fue cambiado a {laureateActual}"
    
    raise HTTPException(status_code=404, detail="Fecha o categoría no encontrada")

@app.put("/Actualizar_Categoria")

def Actualizar_Categoria(year:int,categoria_Anterior:str,categoria_Nueva:str):
    year = str(year)
    for premio in archivo.get("prizes",[]):
        if premio["year"] == year and premio["category"] == categoria_Anterior:
            premio["category"] = categoria_Nueva
            actualizarArchivo()
            return f"La nueva categoria fue exitosa"
    
    raise HTTPException(status_code=404, detail="Error en el año o en la categoría ingresada")

@app.delete("/Eliminar_Premio")

def Eliminar_Premio(Premiados:Premio):
    premio_dict = Premiados.convertirDict()
    if Premiados in archivo["prizes"]:
        archivo["prizes"].remove(premio_dict)
        actualizarArchivo()
        return f"El premio se ha eliminado"
    else:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, porque el premio no existe")