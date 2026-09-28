from fastapi import FastAPI
from routers import users # Import the users router

app = FastAPI(title="Terrain Express API")

# Connect the users router
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Serveur backend Terrain Express en ligne"}