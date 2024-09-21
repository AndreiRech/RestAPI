from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import String, cast, func
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
    
    Não recomendada a utilização pois o tempo de espera é extremamente alto.

    - **Exemplo de Resposta:**
      ```json
      [
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
        },
        {
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

@router.get('/name/{game_name}', response_model=Game, status_code=200)
async def game(
    game_name: Annotated[str, Path(title='O Nome do jogo')],
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
      GET /games/Cuphead
      ```

    - **Exemplo de Resposta:**
      ```json
      {
        "about": "Cuphead is a classic run and gun action game heavily focused on boss battles. Inspired by cartoons of the 1930s, [...]",
        "price": 19.99,
        "positive_rev": 107896,
        "achievements": 42,
        "categories": "Single-player,Multi-player,Co-op,Shared/Split Screen Co-op,Shared/Split Screen,Steam Achievements,Full controller support,Steam Trading Cards,Steam Cloud,Remote Play on Phone,Remote Play on Tablet,Remote Play on TV,Remote Play Together",
        "tags": "Difficult,Cartoon,Platformer,Co-op,Great Soundtrack,Local Co-Op,2D,Hand-drawn,Multiplayer,Indie,Retro,Cartoony,Bullet Hell,Action,Shoot 'Em Up,Side Scroller,Singleplayer,Colorful,Funny,Atmospheric",
        "id": 3812,
        "estimated_owners": "2000000 - 5000000",
        "name": "Cuphead",
        "release_date": "Sep 29, 2017",
        "metacritic_score": 88,
        "negative_rev": 3869,
        "average_playtime": 763,
        "genres": "Action,Indie"
      }
      ```

    - **Código de Status:**
      - `200 OK`: O jogo foi encontrado e a resposta contém os dados do jogo.
      - `404 Not Found`: O jogo com o ID fornecido não foi encontrado.
    """
    
    clean_game_name = game_name.replace(" ", "").lower()

    query = select(Game).where(func.lower(func.replace(Game.name, " ", "")) == clean_game_name)
    result = session.exec(query).first()
    
    print(f"Comparando com CLEAN_NAME: {clean_game_name}")
    print(f"Comparando com RESULT : {result}")
    
    if result is None:
      raise HTTPException(status_code=404, detail='Jogo não encontrado')
    
    return result
  
@router.get('/id/{game_id}', response_model=Game, status_code=200)
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
      GET /games/2264
      ```

    - **Exemplo de Resposta:**
      ```json
      {
        "about": "Game of the Year EDITION The Witcher 3: Wild Hunt Game of the Year edition [...]",
        "price": 0,
        "positive_rev": 0,
        "achievements": 78,
        "categories": "Single-player,Steam Achievements,Full controller support,Steam Trading Cards,Steam Cloud",
        "tags": "",
        "id": 2264,
        "estimated_owners": "0 - 0",
        "name": "The Witcher 3: Wild Hunt - Game of the Year Edition",
        "release_date": "Aug 29, 2016",
        "metacritic_score": 0,
        "negative_rev": 0,
        "average_playtime": "0",
        "genres": "RPG"
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
        - URL: `/search/?q=Counter-Strike:`
        - Descrição: Busca jogos que contenham "Counter-Strike" em qualquer um dos campos pesquisados.

    - **Exemplo de Resposta:**
      ```json
      [
        {
          "about": "With its extensive Tour of Duty campaign, a near-limitless number of skirmish modes, [...]",
          "price": 9.99,
          "positive_rev": 19314,
          "achievements": 0,
          "categories": "Single-player,Multi-player,Valve Anti-Cheat enabled",
          "tags": "Action,FPS,Shooter,Multiplayer,First-Person,Singleplayer,Classic,Tactical,[...]",
          "id": 9908,
          "estimated_owners": "5000000 - 10000000",
          "name": "Counter-Strike: Condition Zero",
          "release_date": "Mar 1, 2004",
          "metacritic_score": 65,
          "negative_rev": 1871,
          "average_playtime": 1523,
          "genres": "Action"
        },
        {
          "about": "THE NEXT INSTALLMENT OF THE WORLD'S # 1 ONLINE ACTION GAME Counter-Strike: Source blends [...]",
          "price": 9.99,
          "positive_rev": 135151,
          "achievements": 147,
          "categories": "Multi-player,Cross-Platform Multiplayer,Steam Achievements,[...]",
          "tags": "Shooter,Action,FPS,Multiplayer,Team-Based,First-Person,Tactical,[...]",
          "id": 21611,
          "estimated_owners": "10000000 - 20000000",
          "name": "Counter-Strike: Source",
          "release_date": "Nov 1, 2004",
          "metacritic_score": 88,
          "negative_rev": 5348,
          "average_playtime": 9171,
          "genres": "Action"
        },
        {
          "about": "With its extensive Tour of Duty campaign, a near-limitless [...]",
          "price": 9.99,
          "positive_rev": 13442,
          "achievements": 0,
          "categories": "Single-player,Multi-player,Valve Anti-Cheat enabled",
          "tags": "Action,FPS,Shooter,Multiplayer,First-Person,Classic,Singleplayer, [...]",
          "id": 40951,
          "estimated_owners": "10000000 - 20000000",
          "name": "Counter-Strike: Condition Zero",
          "release_date": "Mar 1, 2004",
          "metacritic_score": 65,
          "negative_rev": 1535,
          "average_playtime": 1321,
          "genres": "Action"
        },
        {
          "about": "Counter-Strike: Global Offensive (CS: GO) expands upon the team-based action gameplay [...]'",
          "price": 0,
          "positive_rev": 5764420,
          "achievements": 167,
          "categories": "Multi-player,Steam Achievements,Full controller support,Steam Trading Cards,[...]",
          "id": 46159,
          "estimated_owners": "50000000 - 100000000",
          "name": "Counter-Strike: Global Offensive",
          "release_date": "Aug 21, 2012",
          "metacritic_score": 83,
          "negative_rev": 766677,
          "average_playtime": 30484,
          "genres": "Action,Free to Play"
        }
      ]
      ```
    """
    stmt = select(Game)
    
    if q:
      q = q.strip().lower()
        
      search_fields = [
        Game.name.ilike(f'%{q}%'),
        cast(Game.price, String).ilike(f'%{q}%'),
        cast(Game.metacritic_score, String).ilike(f'%{q}%'),
        Game.categories.ilike(f'%{q}%') if Game.categories is not None else None,
        Game.genres.ilike(f'%{q}%') if Game.genres is not None else None,
        Game.tags.ilike(f'%{q}%') if Game.tags is not None else None
      ]
        
      search_conditions = [field for field in search_fields if field is not None]
      stmt = stmt.where(or_(*search_conditions))
    
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
        "about": "A popular tactical shooter game.",
        "price": 59.99,
        "positive_rev": 15000,
        "achievements": 50,
        "categories": "Shooter",
        "tags": "multiplayer, tactical",
        "id": 1334103,
        "estimated_owners": "10 - 2000",
        "name": "Counter-Strike",
        "release_date": "Aug 20, 2024",
        "metacritic_score": 85,
        "negative_rev": 500,
        "average_playtime": "120",
        "genres": "Action"
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
) -> dict:
  """
  Deleta um jogo com base no ID fornecido.
  
  - **id**: ID do jogo a ser deletado. Deve ser um valor numérico inteiro.
  - **session**: Dependência que fornece a sessão do banco de dados.
    
  Retorna uma mensagem indicando que o jogo foi deletado com sucesso.
    
  - Se o jogo com o ID especificado não for encontrado, retorna um erro 404.
  - Se houver um erro ao deletar o jogo, retorna um erro 500.

  - **Exemplo de Requisição:**
    ```http
    DELETE /games/2264
    ```

  - **Exemplo de Resposta:**
    ```json
      "message": "Jogo deletado com sucesso.",
      "game": {
        "about": "Game of the Year EDITION The Witcher 3: Wild Hunt Game of the Year edition [...]",
        "price": 0,
        "positive_rev": 0,
        "achievements": 78,
        "categories": "Single-player,Steam Achievements,Full controller support,Steam Trading Cards,Steam Cloud",
        "tags": "",
        "id": 2264,
        "estimated_owners": "0 - 0",
        "name": "The Witcher 3: Wild Hunt - Game of the Year Edition",
        "release_date": "Aug 29, 2016",
        "metacritic_score": 0,
        "negative_rev": 0,
        "average_playtime": "0",
        "genres": "RPG"
      }
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
      "id": 46160
      {
        "name": "Counter-Strike: Global Offensive",
        "about": "Jogo de dar bala",
        "release_date": "Aug 21, 2024"
      }
      ```

    - **Exemplo de Resposta:**
      ```json
      {
        "message": "Jogo editado com sucesso",
        "game": {
          "about": "Jogo de dar bala",
          "price": 8.99,
          "positive_rev": 0,
          "achievements": 6,
          "categories": "Multi-player,PvP,Online PvP,Steam Achievements,Full controller support,Stats",
          "tags": "Action,Casual,Flight,Multiplayer,Arcade,Character Customization,3D,Colorful,PvP,Side Scroller,Combat",
          "id": 46160,
          "estimated_owners": "0 - 20000",
          "name": "Counter-Strike: Global Offensive",
          "release_date": "May 31, 2021",
          "metacritic_score": 0,
          "negative_rev": 2,
          "average_playtime": 0,
          "genres": "Action,Casual"
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