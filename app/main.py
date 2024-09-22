from fastapi import FastAPI
from app.database.db import init_db

from app.routers import games, welcome

app = FastAPI()

def init(app: FastAPI) -> None:
    """
    Inicializa as rotas da aplicação
    """
    init_db()
    app.include_router(games.router)
    app.include_router(welcome.router)
    
init(app)