import csv
from pathlib import Path

from fastapi import HTTPException, UploadFile

UPLOAD_DIR = Path("app/static")


async def save_file(file: UploadFile) -> Path:
    """
    Salva o arquivo no sistema
    """
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    try:  
        for existing_file in UPLOAD_DIR.glob("*"):
            if existing_file.is_file():
                existing_file.unlink()

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}")


def read_csv_file(file_path: Path):
    """
    Abre o arquivo e retorna todas as linha do mesmo
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]