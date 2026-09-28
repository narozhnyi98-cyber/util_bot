import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "coefficients.json"


def load_coefficients() -> dict:
    """Загружает справочник коэффициентов из JSON-файла."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_coefficient(block: dict, engine_power: int) -> float | None:
    """
    Универсальная функция поиска коэффициента внутри блока.
    Поддерживает два формата:
    1. {"power_ranges": [{"max_power": 160, "coeff": 0.17}, ...]}
    2. {"coeff": 3.5}
    """
    if "power_ranges" in block:
        for r in block["power_ranges"]:
            if engine_power <= r["max_power"]:
                return r["coeff"]
        return block["power_ranges"][-1]["coeff"]

    if "coeff" in block:
        return block["coeff"]

    return None


def calculate_util(data: dict) -> dict | None:
    """
    Принимает словарь с ключами:
    category, importer, age, engine_volume, engine_power.
    Возвращает словарь с base, coefficient, total или None при ошибке.
    """
    config = load_coefficients()
    base_rates = config["base_rates"]
    coefficients = config["coefficients"]

    category = data.get("category")
    importer = data.get("importer")
    age = data.get("age")
    engine_volume = data.get("engine_volume")
    engine_power = data.get("engine_power")

    base = base_rates.get(category)
    if base is None:
        return None

    try:
        block = coefficients[category][importer][age]
    except KeyError:
        return None

    coeff = find_coefficient(block, engine_power)
    if coeff is None:
        return None

    total = base * coeff

    return {
        "base": base,
        "coefficient": coeff,
        "total": total,
        "category": category,
        "importer": importer,
        "age": age,
        "engine_volume": engine_volume,
        "engine_power": engine_power,
    }
