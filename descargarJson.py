import requests


url = "https://api.nobelprize.org/v1/prize.json"
archivoJson = "prize.json"

def descargarJson(url, save_path):
    try:
        # Hacer la solicitud GET a la URL
        response = requests.get(url)
        # Comprobar si la solicitud fue exitosa
        response.raise_for_status()
        # Guardar el contenido JSON en un archivo
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"JSON descargado y guardado en {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error descargando el JSON: {e}")

descargarJson(url,archivoJson)