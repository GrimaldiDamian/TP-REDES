from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/LeerArchivo")

def LeerArchivo():
    with open("prize.json", 'r') as file:
        dicJson = json.load(file)
    return dicJson