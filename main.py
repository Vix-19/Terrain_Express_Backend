from fastapi import FastAPI

app = FastAPI(title="Terrain Express API")

@app.get("/")
def root():
    return {"message": "Serveur backend Terrain Express en ligne"}