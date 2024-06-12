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

diccionario = diccJson(archivoJson)
CantidadObjeto = cantObjeto(diccionario)
nombresPropiedades = propiedades(diccionario)
print(nombresPropiedades)