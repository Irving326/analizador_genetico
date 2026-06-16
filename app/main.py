from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app import analizer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

#Conexion
#incluir las rutas de analizer.py en el servidor principal
app.include_router(analizer.router, prefix="/analysis", tags="Genetic Analysis")

@app.get("/")
async def root(request: Request):
    
    return templates.TemplateResponse(request=request, name="index.html")

#Ejecuta el servidor en el puerto 8000
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)