from typing import Optional
from sqlmodel import SQLModel, Field

class GameBase(SQLModel):
    name: str
    release_date: str
    estimated_owners: str
    price: float
    about: Optional[str]
    metacritic_score: int
    positive_rev: int
    negative_rev: int
    achievements: int
    average_playtime: int
    categories: str
    genres: str
    tags: str
    
class Game(GameBase, table=True):
    id: int = Field(default=None, primary_key=True)