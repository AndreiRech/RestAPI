from fastapi import FastAPI

from app.routers import csv

app = FastAPI()

def init(app: FastAPI) -> None:
    """
    Inicializa as rotas da aplicação
    """
    app.include_router(csv.router)
    
init(app)