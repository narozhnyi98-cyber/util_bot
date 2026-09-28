COEFFICIENTS = {
    "base_rates": {
        "Легковой": 20000,
        "Грузовой": 150000,
        "Автобус": 150000,
        "Спецтехника": 172500,
    },
    "coefficients": {
        "Легковой": {
            "Физическое лицо": {
                "До 3 лет": {"power_ranges": [
                    {"max_power": 160, "coeff": 0.17},
                    {"max_power": 190, "coeff": 92.40},
                    {"max_power": 220, "coeff": 109.68},
                    {"max_power": 250, "coeff": 129.96},
                    {"max_power": 280, "coeff": 153.96},
                    {"max_power": 9999, "coeff": 182.40},
                ]},
                "Старше 3 лет": {"power_ranges": [
                    {"max_power": 160, "coeff": 0.26},
                    {"max_power": 190, "coeff": 129.72},
                    {"max_power": 220, "coeff": 151.20},
                    {"max_power": 250, "coeff": 176.16},
                    {"max_power": 280, "coeff": 205.20},
                    {"max_power": 9999, "coeff": 239.04},
                ]},
            },
            "Юридическое лицо": {
                "До 3 лет": {"power_ranges": [
                    {"max_power": 160, "coeff": 40.04},
                    {"max_power": 190, "coeff": 45.00},
                    {"max_power": 220, "coeff": 47.64},
                    {"max_power": 250, "coeff": 50.52},
                    {"max_power": 280, "coeff": 57.12},
                    {"max_power": 310, "coeff": 64.56},
                    {"max_power": 340, "coeff": 72.96},
                    {"max_power": 370, "coeff": 83.16},
                    {"max_power": 400, "coeff": 94.80},
                    {"max_power": 430, "coeff": 108.00},
                    {"max_power": 460, "coeff": 123.24},
                    {"max_power": 500, "coeff": 140.40},
                    {"max_power": 9999, "coeff": 160.08},
                ]},
                "Старше 3 лет": {"power_ranges": [
                    {"max_power": 160, "coeff": 70.44},
                    {"max_power": 190, "coeff": 74.64},
                    {"max_power": 220, "coeff": 79.20},
                    {"max_power": 250, "coeff": 83.88},
                    {"max_power": 280, "coeff": 91.92},
                    {"max_power": 310, "coeff": 100.56},
                    {"max_power": 340, "coeff": 110.16},
                    {"max_power": 370, "coeff": 120.60},
                    {"max_power": 400, "coeff": 132.00},
                    {"max_power": 430, "coeff": 144.60},
                    {"max_power": 460, "coeff": 158.40},
                    {"max_power": 500, "coeff": 173.40},
                    {"max_power": 9999, "coeff": 189.84},
                ]},
            },
        },
        "Грузовой": {
            "Физическое лицо": {
                "До 3 лет": {"coeff": 1.0},
                "Старше 3 лет": {"coeff": 1.5},
            },
            "Юридическое лицо": {
                "До 3 лет": {"coeff": 3.0},
                "Старше 3 лет": {"coeff": 4.0},
            },
        },
        "Автобус": {
            "Физическое лицо": {
                "До 3 лет": {"coeff": 1.0},
                "Старше 3 лет": {"coeff": 1.5},
            },
            "Юридическое лицо": {
                "До 3 лет": {"coeff": 3.0},
                "Старше 3 лет": {"coeff": 4.0},
            },
        },
        "Спецтехника": {
            "Физическое лицо": {
                "До 3 лет": {"coeff": 1.5},
                "Старше 3 лет": {"coeff": 2.0},
            },
            "Юридическое лицо": {
                "До 3 лет": {"coeff": 4.0},
                "Старше 3 лет": {"coeff": 5.0},
            },
        },
    },
}


def find_coefficient(block: dict, engine_power: int):
    if "power_ranges" in block:
        for r in block["power_ranges"]:
            if engine_power <= r["max_power"]:
                return r["coeff"]
        return block["power_ranges"][-1]["coeff"]
    if "coeff" in block:
        return block["coeff"]
    return None


def calculate_util(data: dict):
    base_rates = COEFFICIENTS["base_rates"]
    coefficients = COEFFICIENTS["coefficients"]

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
