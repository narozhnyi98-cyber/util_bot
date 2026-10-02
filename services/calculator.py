import logging

logger = logging.getLogger(__name__)


# Базовые ставки
BASE_RATES = {
    "Легковой": 20000,
    "Грузовой": 150000,
    "Автобус": 150000,
    "Спецтехника": 172500,
}

# ─── Коэффициенты утильсбора ───

# ДВС (порог льготы 160 л.с.)
UTIL_COEF_ICE_NEW = [
    (160, 0.17), (190, 92.40), (220, 109.68),
    (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_ICE_OLD = [
    (160, 0.26), (190, 129.72), (220, 151.20),
    (250, 176.16), (280, 205.20), (9999, 239.04),
]

# Электромобили (порог льготы 80 л.с. = 58.84 кВт)
UTIL_COEF_EV_NEW = [
    (80, 0.17),
    (9999, 15.73),
]
UTIL_COEF_EV_OLD = [
    (80, 0.26),
    (9999, 15.73),
]

# Гибриды (порог льготы 160 л.с.)
UTIL_COEF_HEV_NEW = [
    (160, 0.17), (190, 92.40), (220, 109.68),
    (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_HEV_OLD = [
    (160, 0.26), (190, 129.72), (220, 151.20),
    (250, 176.16), (280, 205.20), (9999, 239.04),
]

# Юрлица — упрощённые коэффициенты (для категорий, где нет power_ranges)
UTIL_COEF_LEGAL = {
    "Легковой": {"До 3 лет": 2.41, "Старше 3 лет": 3.5},
    "Грузовой": {"До 3 лет": 3.0, "Старше 3 лет": 4.0},
    "Автобус": {"До 3 лет": 3.0, "Старше 3 лет": 4.0},
    "Спецтехника": {"До 3 лет": 4.0, "Старше 3 лет": 5.0},
}

KW_TO_HP = 1.35962  # 1 кВт = 1.35962 л.с.


def calculate_util(data: dict) -> dict | None:
    """
    Расчёт утильсбора.
    data: {
        engine_type: "ICE" | "EV" | "HEV",
        category, importer, age,
        engine_volume, engine_power (в л.с.),
        power_kw (для EV — если передана в кВт),
    }
    """
    engine_type = data.get("engine_type", "ICE")
    category = data.get("category", "Легковой")
    importer = data.get("importer")
    age = data.get("age")
    engine_volume = data.get("engine_volume", 0)
    engine_power = data.get("engine_power", 0)

    base = BASE_RATES.get(category)
    if base is None:
        return None

    # ─── Юрлица: упрощённые коэффициенты ───
    if importer == "Юридическое лицо":
        coef_table = UTIL_COEF_LEGAL.get(category, UTIL_COEF_LEGAL["Легковой"])
        coef = coef_table.get(age)
        if coef is None:
            return None
        total = base * coef
        return {
            "engine_type": engine_type,
            "category": category,
            "importer": importer,
            "age": age,
            "engine_volume": engine_volume,
            "engine_power": engine_power,
            "base": base,
            "coefficient": coef,
            "total": total,
        }

    # ─── Физлица: по типу двигателя ───
    if engine_type == "EV":
        table = UTIL_COEF_EV_NEW if age == "До 3 лет" else UTIL_COEF_EV_OLD
    elif engine_type == "HEV":
        table = UTIL_COEF_HEV_NEW if age == "До 3 лет" else UTIL_COEF_HEV_OLD
    else:
        table = UTIL_COEF_ICE_NEW if age == "До 3 лет" else UTIL_COEF_ICE_OLD

    coef = None
    for max_power, c in table:
        if engine_power <= max_power:
            coef = c
            break
    if coef is None:
        coef = table[-1][1]

    total = base * coef
    return {
        "engine_type": engine_type,
        "category": category,
        "importer": importer,
        "age": age,
        "engine_volume": engine_volume,
        "engine_power": engine_power,
        "base": base,
        "coefficient": coef,
        "total": total,
    }
