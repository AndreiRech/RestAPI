# 🔖 ALUNOS

- [Andrei Rech | 23102140](https://github.com/AndreiRech) 
- [Urien Nolasco | 23102720](https://github.com/UrienNolasco)

# 📚 INTRODUÇÃO

Criação de uma FastAPI com o objetivo de realizar operações em um conjunto de dados.

# 🛠 PRÉ REQUISITOS

É necessário possuir a linguagem [Python](https://www.python.org/downloads/) instalada no computador (de preferência 3.12.x - mas pode funcionar em superiores).

Outra ferramente muito importante é o gerenciador de pacotes do Python, o [Pip](https://pypi.org/project/pip/).


# ⚙ INICIALIZAÇÃO APLICAÇÃO

Para a realização do projeto, utilizamos alguns pacotes adicionais. Segue a baixo a lista de pacotes a serem instalados e seus comandos:

- *FastAPI*
```
pip install fastapi
```

- *Uvicorn*
```
pip install fastapi uvicorn
```

*Pandas*
```
pip install pandas

```

*SQLModel*
```
pip install sqlmodel

```

Com tudo instalado, informe o comando para rodar a aplicação:
```
uvicorn app.main:app --reload
```

# CONSUMINDO A API

Para consumir a API, será necessário realizar algumas alterações

# O QUE FAZER

### Parte 1
- [X] Escolher conjunto de dados
- [X] Tratar conjunto, removendo informações desnecessárias 
- [X] Criação da API que permite:
    - [X] Consulta
    - [X] Atualização
    - [X] Inserção
    - [X] Deleção

### Parte 2
- [X] Documentar o projeto utilizando Postman
    - [X] Exemplos de requisições

### Parte 3
- [X] Hospedar a API na web

### Parte 4
- [X] Criação de um script Python que seja capaz de consumir todas as funcionalidades da API
