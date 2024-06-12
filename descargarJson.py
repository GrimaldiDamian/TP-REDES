import requests
import json


url = "https://api.nobelprize.org/v1/prize.json"
archivoJson = "prize.json"

def descargarJson(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"JSON descargado y guardado en {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error descargando el JSON: {e}")

def transformarloDic(archivo):
    with open (archivo) as file:
        dicJson = json.load(file)
    return dicJson

descargarJson(url,archivoJson)
transformarloDic(archivoJson)