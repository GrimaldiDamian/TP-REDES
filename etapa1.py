import json

archivoJson = "prize.json"

def diccJson(archivo):
    with open (archivo) as file:
        dicJson = json.load(file)
    return dicJson

def cantObjeto(dicc):
    return len(dicc)

def propiedades(dicc):
    NomProp = {}

    for valores in dicc.values():
        for dicPropiedades in valores:
            for propiedades, atributos in dicPropiedades.items():
                if propiedades not in NomProp:
                    if isinstance(atributos, list):
                        NomProp[propiedades] = {}
                        for atributo in atributos:
                            for prop in atributo:
                                if prop not in NomProp[propiedades]:
                                    NomProp[propiedades][prop] = atributo[prop].__class__.__name__
                    else:
                        NomProp[propiedades] = atributos.__class__.__name__
    
    return NomProp

def Informe(cantObjeto,propiedades):
    print (f"El archivo json cuenta con un total de {cantObjeto}, y posee los siguientes atributos:")
    for claves, valores in propiedades.items():
        if claves == "laureates":
            print(f"Y {claves} posee los siguientes atributos y tipos: ")
            for laureate_props in valores.items():
                print(f"\t{laureate_props[0]} y su tipo: {laureate_props[1]}")
        else:
            print(f"{claves} y su tipo: {valores}")
diccionario = diccJson(archivoJson)
CantidadObjeto = cantObjeto(diccionario)
nombresPropiedades = propiedades(diccionario)
Informe(CantidadObjeto,nombresPropiedades)