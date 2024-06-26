#Etapa 1: funcion para descargar archivo Json

import requests

def descargarJson(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"JSON descargado y guardado en {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error descargando el JSON: {e}")
