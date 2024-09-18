from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from app.models.game import Game, GameBase, GameUpdate
from sqlmodel import Session, or_, select
from app.database.db import get_session

router = APIRouter(prefix="/games", tags=["Games"])

@router.get('', response_model=List[Game], status_code=200)
async def games(
    session: Session = Depends(get_session)
) -> list[Game]:
    """
    Retorna uma lista de todos os jogos no banco de dados.
    
    - **session**: Dependência que fornece a sessão do banco de dados.
    
    Retorna uma lista de objetos `Game` representando os jogos.

    - **Exemplo de Resposta:**
      ```json
      [
        {
          "id": 1,
          "name": "Counter-Strike",
          "release_date": "Aug 20, 2024",
          "estimated_owners": "10 - 2000",
          "price": 59.99,
          "about": "A popular tactical shooter game.",
          "metacritic_score": 85,
          "positive_rev": 15000,
          "negative_rev": 500,
          "achievements": 50,
          "average_playtime": 120,
          "categories": "Shooter",
          "genres": "Action",
          "tags": "multiplayer, tactical"
        },
        {
          "id": 2,
          "name": "The Witcher 3",
          "release_date": "May 19, 2015",
          "estimated_owners": "5,000,000 - 10,000,000",
          "price": 39.99,
          "about": "An open-world RPG set in a fantastical universe.",
          "metacritic_score": 93,
          "positive_rev": 20000,
          "negative_rev": 400,
          "achievements": 80,
          "average_playtime": 200,
          "categories": "RPG",
          "genres": "Adventure",
          "tags": "fantasy, open-world"
        }
      ]
      ```
    """
    game_list = session.exec(select(Game)).all()
    return game_list

@router.get('/{game_name}', response_model=Game, status_code=200)
async def game(
    game_name: Annotated[int, Path(title='O Nome do jogo')],
    session: Session = Depends(get_session)
) -> Game:
    """
    Retorna um jogo com base no ID fornecido.
    
    - **game_name**: Nome do jogo a ser recuperado. Deve ser um valor em String.
    - **session**: Dependência que fornece a sessão do banco de dados.
    
    Retorna um objeto `Game` correspondente ao nome fornecido.
    
    - Se o jogo com o nome especificado não for encontrado, retorna um erro 404.

    - **Exemplo de Requisição:**
      ```http
      GET /games/The Witcher 3
      ```

    - **Exemplo de Resposta:**
      ```json
      {
        "id": 1,
        "name": "The Witcher 3",
        "release_date": "Aug 20, 2024",
        "estimated_owners": "10 - 2000",
        "price": 59.99,
        "about": "Jogagando com o bruxão",
        "metacritic_score": 85,
        "positive_rev": 15000,
        "negative_rev": 500,
        "achievements": 50,
        "average_playtime": 120,
        "categories": "RPG",
        "genres": "Action",
        "tags": "singleplayer, fantasy"
      }
      ```

    - **Código de Status:**
      - `200 OK`: O jogo foi encontrado e a resposta contém os dados do jogo.
      - `404 Not Found`: O jogo com o ID fornecido não foi encontrado.
    """
    game = session.get(Game, game_name)
    if game is None:
        raise HTTPException(status_code=404, detail='Jogo não encontrado')
    
    return game
  
@router.get('/{game_id}', response_model=Game, status_code=200)
async def game(
    game_id: Annotated[int, Path(title='O ID do jogo')],
    session: Session = Depends(get_session)
) -> Game:
    """
    Retorna um jogo com base no ID fornecido.
    
    - **game_id**: ID do jogo a ser recuperado. Deve ser um valor numérico inteiro.
    - **session**: Dependência que fornece a sessão do banco de dados.
    
    Retorna um objeto `Game` correspondente ao ID fornecido.
    
    - Se o jogo com o ID especificado não for encontrado, retorna um erro 404.

    - **Exemplo de Requisição:**
      ```http
      GET /games/1
      ```

    - **Exemplo de Resposta:**
      ```json
      {
        "id": 1,
        "name": "Counter-Strike",
        "release_date": "Aug 20, 2024",
        "estimated_owners": "10 - 2000",
        "price": 59.99,
        "about": "A popular tactical shooter game.",
        "metacritic_score": 85,
        "positive_rev": 15000,
        "negative_rev": 500,
        "achievements": 50,
        "average_playtime": 120,
        "categories": "Shooter",
        "genres": "Action",
        "tags": "multiplayer, tactical"
      }
      ```

    - **Código de Status:**
      - `200 OK`: O jogo foi encontrado e a resposta contém os dados do jogo.
      - `404 Not Found`: O jogo com o ID fornecido não foi encontrado.
    """
    game = session.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail='Jogo não encontrado')
    
    return game

@router.get('/search/', response_model=List[Game], status_code=200)
async def search(
    q: Annotated[Optional[str], Query(max_length=40)] = None,
    session: Session = Depends(get_session)
) -> list[Game]:
    """
    Retorna uma lista de jogos que correspondem à busca realizada na query.

    Este endpoint permite pesquisar jogos com base em um termo de pesquisa fornecido. 
    A busca é feita em vários campos do modelo `GameBase`, incluindo:
    - Nome do jogo (`name`)
    - Preço (`price`)
    - Pontuação no Metacritic (`metacritic_score`)
    - Categorias (`categories`)
    - Gêneros (`genres`)
    - Tags (`tags`)

    O parâmetro `q` é um termo de pesquisa opcional. Se fornecido, ele será utilizado para filtrar os resultados que contenham o termo em qualquer um dos campos listados. A pesquisa é realizada de forma case-insensitive.

    - **Parâmetros:**
        - `q` (opcional): Termo de pesquisa para filtrar os jogos. Máximo de 40 caracteres.
        - `session`: Dependência para obter a sessão do banco de dados.

    - **Resposta:**
        - Uma lista de objetos `Game` que correspondem ao termo de pesquisa.

    - **Código de Status:**
        - `200 OK`: A solicitação foi bem-sucedida e a resposta contém a lista de jogos.
        
    - **Exemplo de Requisição:**
        - URL: `/search/?q=Counter:Strike`
        - Descrição: Busca jogos que contenham "Counter-Strike" em qualquer um dos campos pesquisados.

    - **Exemplo de Resposta:**
      ```json
      [
        {
          "id": 1,
          "name": "Counter-Strike",
          "release_date": "Nov 8, 2000",
          "estimated_owners": "5,000,000 - 10,000,000",
          "price": 19.99,
          "about": "A popular tactical shooter game.",
          "metacritic_score": 85,
          "positive_rev": 15000,
          "negative_rev": 500,
          "achievements": 50,
          "average_playtime": 120,
          "categories": "Shooter",
          "genres": "Action",
          "tags": "multiplayer, tactical"
        }
      ]
      ```
    """
    stmt = select(Game)
    
    if q:
        q = q.lower()
        stmt = stmt.where(
            or_(
                Game.name.ilike(f'%{q}%'),
                Game.price.ilike(f'%{q}%'),
                Game.metacritic_score.ilike(f'%{q}%'),
                Game.categories.ilike(f'%{q}%'),
                Game.genres.ilike(f'%{q}%'),
                Game.tags.ilike(f'%{q}%')
            )
        )
    
    game_list = session.exec(stmt).all()
    return game_list

@router.post('', response_model=Game ,status_code=201)
async def create(
    g: GameBase,
    session: Session = Depends(get_session)
) -> Game:
    """
    Cria um novo jogo com base nos dados fornecidos.
    
    - **g**: Dados do novo jogo, fornecidos como um objeto `GameBase`.
    - **session**: Dependência que fornece a sessão do banco de dados.
    
    Retorna o objeto `Game` criado, incluindo o ID gerado.
    
    - Se houver um erro ao adicionar o jogo ao banco de dados, retorna um erro 500.

    - **Exemplo de Requisição:**
      ```json
      {
        "name": "Counter-Strike",
        "release_date": "Aug 20, 2024",
        "estimated_owners": "10 - 2000",
        "price": 59.99,
        "about": "A popular tactical shooter game.",
        "metacritic_score": 85,
        "positive_rev": 15000,
        "negative_rev": 500,
        "achievements": 50,
        "average_playtime": 120,
        "categories": "Shooter",
        "genres": "Action",
        "tags": "multiplayer, tactical"
      }
      ```

    - **Exemplo de Resposta:**
      ```json
      {
        "id": 1,
        "name": "Counter-Strike",
        "release_date": "Aug 20, 2024",
        "estimated_owners": "10 - 2000",
        "price": 59.99,
        "about": "A popular tactical shooter game.",
        "metacritic_score": 85,
        "positive_rev": 15000,
        "negative_rev": 500,
        "achievements": 50,
        "average_playtime": 120,
        "categories": "Shooter",
        "genres": "Action",
        "tags": "multiplayer, tactical"
      }
      ```
    """
    game = Game(**g.model_dump())
    
    session.add(game)
    session.commit()
    session.refresh(game)
    
    return game
    
@router.delete('/delete/{game_id}', status_code=200)
async def delete(
  game_id: Annotated[int, Path(title='O ID do jogo a ser deletado')],
  session: Session = Depends(get_session)
) -> str:
  """
  Deleta um jogo com base no ID fornecido.
  
  - **id**: ID do jogo a ser deletado. Deve ser um valor numérico inteiro.
  - **session**: Dependência que fornece a sessão do banco de dados.
    
  Retorna uma mensagem indicando que o jogo foi deletado com sucesso.
    
  - Se o jogo com o ID especificado não for encontrado, retorna um erro 404.
  - Se houver um erro ao deletar o jogo, retorna um erro 500.

  - **Exemplo de Requisição:**
    ```http
    DELETE /games/1
    ```

  - **Exemplo de Resposta:**
    ```json
    "Jogo deletado com sucesso."
    ```

  - **Código de Status:**
    - `204 No Content`: O jogo foi deletado com sucesso.
    - `404 Not Found`: O jogo com o ID fornecido não foi encontrado.
  """
  
  game = session.get(Game, game_id)
  if game is None:
    raise HTTPException(status_code=404, detail='Jogo não encontrado')
    
  session.delete(game)
  session.commit()
    
  return {"message": "Jogo deletado com sucesso", "game": game}

@router.put('/edit/{game_id}', status_code=200)
async def edit(
  game_id: Annotated[int, Path(title='O ID do jogo a ser editado')],
  game_update: GameUpdate,
  session: Session = Depends(get_session)
) -> dict:
  """
    Edita um jogo existente com base no ID fornecido e nos novos dados.

    - **game_id**: O ID do jogo que deve ser editado, passado como parâmetro na URL.
    - **game_update**: Dados a serem atualizados no jogo, fornecidos como um objeto `GameUpdate`.
    - **session**: Dependência que fornece a sessão do banco de dados.
    
    Retorna uma mensagem de sucesso e os dados atualizados do jogo.

    - Se o jogo com o `game_id` fornecido não for encontrado, retorna um erro 404.

    - **Exemplo de Requisição:**
      ```json
      {
        "title": "Counter-Strike: Global Offensive",
        "description": "A tactical shooter game",
        "release_date": "Aug 21, 2024"
      }
      ```

    - **Exemplo de Resposta:**
      ```json
      {
        "message": "Jogo editado com sucesso",
        "game": {
          "id": 1,
          "title": "Counter-Strike: Global Offensive",
          "description": "A tactical shooter game",
          "release_date": "Aug 21, 2024"
        }
      }
      ```
  """
  
  game = session.get(Game, game_id)
  if game is None:
    raise HTTPException(status_code=404, detail='Jogo não encontrado')
  
  if game_update.name is not None:
    game.name = game_update.name
  if game_update.price is not None:
    game.price = game_update.price
  if game_update.about is not None:
    game.about = game_update.about
  if game_update.metacritic_score is not None:
    game.metacritic_score = game_update.metacritic_score
  
  session.commit()
  session.refresh(game)
    
  return {"message": "Jogo editado com sucesso", "game": game}