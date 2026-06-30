import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "requests.json"


def ensure_data_file() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("{}", encoding="utf-8")


def load_requests() -> dict[str, Any]:
    ensure_data_file()
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            return {}
    except json.JSONDecodeError:
        return {}


def save_requests(data: dict[str, Any]) -> None:
    ensure_data_file()
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
