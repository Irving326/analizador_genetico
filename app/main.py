from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
#importar el archivo analizer.py 
from app import analizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

#Conexion
#incluir las rutas de analizer.py en el servidor principal
app.include_router(analizer.router, prefix="/analysys", tags="Genetic Analysis")

@app.get("/")
async def root():
    return {"message": "¡Bienvenido al Analizador Genético!"}

#Ejecuta el servidor en el puerto 8000
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)