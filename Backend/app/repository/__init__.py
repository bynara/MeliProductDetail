import json
import os
from pydantic import ValidationError
from functools import lru_cache


class InvalidJSONStructure(Exception):
    pass

def load_and_validate_json(filepath: str) -> list[dict]:
    """
    Loads a JSON file, validates its structure, and deserializes the content using a Pydantic BaseModel.

    :param filepath: Path to the JSON file.
    :param model: Pydantic BaseModel class to validate the data.
    :return: List of validated dicts.
    :raises FileNotFoundError: If the file does not exist.
    :raises json.JSONDecodeError: If the file is not valid JSON.
    :raises InvalidJSONStructure: If the structure is not as expected.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filepath}") from e
    except OSError as e:
        raise OSError(f"Error opening file: {filepath} - {e}") from e
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON in {filepath}: {e.msg}", e.doc, e.pos)
    try:
        if isinstance(data, list):
            return data
        # Single object
        return [data]
    except ValidationError as e:
        raise InvalidJSONStructure(f"Invalid JSON structure: {e}")
    
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
DATA_DIR = os.path.normpath(DATA_DIR)

@lru_cache(maxsize=1)
def get_db_data() -> dict[str, list[dict]]:
    products_path = os.path.join(DATA_DIR, "products.json")
    categories_path = os.path.join(DATA_DIR, "categories.json")
    sellers_path = os.path.join(DATA_DIR, "sellers.json")
    payment_methods_path = os.path.join(DATA_DIR, "payment_methods.json")
    reviews_path = os.path.join(DATA_DIR, "reviews.json")
    data_files = {
        "products": products_path,
        "categories": categories_path,
        "sellers": sellers_path,
        "payment_methods": payment_methods_path,
        "reviews": reviews_path,
    }
    db: dict[str, list[dict]] = {}
    for key, path in data_files.items():
        db[key] = load_and_validate_json(path)  # Validate the structure
    return db

def get_db() -> dict[str, list[dict]]:
    return get_db_data()

def get_table(db: dict, table: str) -> list[dict]:
    if table not in db:
        raise ValueError(f"Table {table} does not exist in the database.")
    return db[table]

def get_all(db: dict, table: str) -> list[dict]:
    return get_table(db, table)

def get_item_by_id(db: dict, table: str, item_id: int) -> dict:
    items = get_table(db, table)
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        raise ValueError(f"Item with id {item_id} not found in table {table}.")
    return item