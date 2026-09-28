import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "coefficients.json"


def load_coefficients() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


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
        if importer == "Физическое лицо":
            power_ranges = coefficients[category][importer][age]["power_ranges"]
            coeff = None
            for r in power_ranges:
                if engine_power <= r["max_power"]:
                    coeff = r["coeff"]
                    break
            if coeff is None:
                coeff = power_ranges[-1]["coeff"]
        else:
            coeff = coefficients[category][importer][age]["coeff"]
    except KeyError:
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
        "engine_power": engine_power
    }