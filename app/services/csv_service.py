import csv
from fastapi import HTTPException, Path
from sqlmodel import Session
from app.models.game import Game

def insert_csv_data(file_path: Path, session: Session) -> None:
    """
    Lê dados de um arquivo CSV e insere no banco de dados.
    """
    data = read_csv_file(file_path)
    
    games = []
    for row in data:
        try:
            game = Game(
                name=row['Name'],
                release_date=row['Release date'],
                estimated_owners=row['Estimated owners'],
                price=float(row['Price']),
                about=row.get('About the game'),
                metacritic_score=int(row['Metacritic score']),
                positive_rev=int(row['Positive']),
                negative_rev=int(row['Negative']),
                achievements=int(row['Achievements']),
                average_playtime=int(row['Average playtime forever']),
                categories=row['Categories'],
                genres=row['Genres'],
                tags=row['Tags']
            )
            games.append(game)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Erro ao processar a linha: {row}. Erro: {e}")
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Campo ausente: {e}")
    
    session.add_all(games)
    session.commit()
        
def read_csv_file(file_path: Path):
    """
    Realiza a leitura do csv e retorna todas as linhas para serem adicionadas no banco de dados.
    """
    csv.field_size_limit(1000000) 
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]