import requests

BASE_URL = 'https://restapi-v1go.onrender.com/games'

def get_all_games():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Não foi possível obter os jogos."}
    
def get_game_by_id(game_id):
    response = requests.get(f"{BASE_URL}/id/{game_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Jogo não encontrado."}

def get_game_by_name(game_name):
    response = requests.get(f"{BASE_URL}/search/?q={game_name}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Erro ao buscar jogo pelo nome."}

def search_games(query):
    response = requests.get(f"{BASE_URL}/search/?q={query}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Erro na busca de jogos."}

def create_game(game_data):
    response = requests.post(BASE_URL, json=game_data)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": "Erro ao criar o jogo."}

def delete_game(game_id):
    response = requests.delete(f"{BASE_URL}/delete/{game_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Erro ao deletar o jogo."}

def edit_game(game_id, game_data):
    response = requests.put(f"{BASE_URL}/edit/{game_id}", json=game_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Erro ao editar o jogo."}

def main():
    jogo = {
        "name": "Counter-Strike 800",
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
    
    editar = {
        "name": "Counter-Strike: Global Offensive",
        "about": "Jogo de dar bala",
        "release_date": "Aug 21, 2024"
    }
    
    # Get games/
    # print(get_all_games())
    
    # Get games/id/2264
    print('Get games/id/\n')
    print(get_game_by_id(2265))
    print('\n')
    
    # Get games/name/Cuphead
    print('Get games/name/\n')
    print(get_game_by_name('Cuphead'))
    print('\n')
    
    # Get games/search/?q=Counter-Strike:
    print('Get games/search/\n')
    print(search_games('Counter-Strike:'))
    print('\n')
    
    # Post games/
    print('Post games/\n')
    print(create_game(jogo))
    print('\n')
        
    # Delete games/delete/2264
    print('Delete games/delete/\n')
    print(delete_game(2265))
    print('\n')
    
    # Patch games/edit/46160
    print('Patch games/edit/\n')
    print(edit_game(46160, editar))
    print('\n')
    
main()