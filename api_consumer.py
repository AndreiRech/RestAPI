import requests

BASE_URL = 'https://educational-armadillo-goat-api-7aa7423b.koyeb.app/games'

def get_welcome_message():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Não foi possível obter a mensagem de boas-vindas."}

def get_all_games():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Não foi possível obter os jogos."}

def get_game_by_id(game_id):
    response = requests.get(f"{BASE_URL}/{game_id}")
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
    response = requests.delete(f"{BASE_URL}/{game_id}")
    if response.status_code == 204:  # Sem conteúdo para sucesso na deleção
        return {"message": "Jogo deletado com sucesso."}
    else:
        return {"error": "Erro ao deletar o jogo."}

def edit_game(game_id, game_data):
    response = requests.put(f"{BASE_URL}/edit/{game_id}", json=game_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Erro ao editar o jogo."}

if __name__ == "__main__":
    
    # Dados do novo jogo
    new_game = {
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
    
    # Adiciona o novo jogo
    print(create_game(new_game))
    
    # Realiza a pesquisa pelo nome
    print(get_game_by_name("Counter-Strike"))  # Usando a busca pelo nome


    print(get_game_by_id(1))

    print(delete_game(1))

    print(get_all_games())