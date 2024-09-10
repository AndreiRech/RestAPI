from fastapi import HTTPException, UploadFile

from app.utils.file_handler import read_csv_file, save_file


async def process_csv(file: UploadFile):
    """
    Processa o arquivo, valida se não está vazio e retorna as linhas
    """
    file_path = await save_file(file)

    try:
        rows = read_csv_file(file_path)

        if len(rows) == 0:
            raise HTTPException(
                status_code=422, detail="CSV inválido. O arquivo precisa ter conteúdo."
            )
            
        print(rows)

        return rows

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro {str(e)} ao processar o CSV."
        )