
from fastapi import FastAPI

app = FastAPI()

@app.get("/weather/{airport}")
def weather(airport:str):
    return {"airport":airport,"event":"Storm","severity":"High"}
