from fastapi import FastAPI
from routers import users, pitches, bookings, matches

app = FastAPI(title="Terrain Express API")

# Connect routers
app.include_router(users.router)
app.include_router(pitches.router)
app.include_router(bookings.router)
app.include_router(matches.router)

@app.get("/")
def root():
    return {"message": "Serveur backend Terrain Express en ligne"}