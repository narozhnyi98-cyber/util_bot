import logging

logger = logging.getLogger(__name__)

BASE_RATES = {
    "Легковой": 20000,
    "Грузовой": 150000,
    "Автобус": 150000,
    "Спецтехника": 172500,
}

# ─── Коэффициенты утильсбора для ДВС ───
UTIL_COEF_ICE_NEW = [(160, 0.17), (190, 92.40), (220, 109.68), (250, 129.96), (280, 153.96), (9999, 182.40)]
UTIL_COEF_ICE_OLD = [(160, 0.26), (190, 129.72), (220, 151.20), (250, 176.16), (280, 205.20), (9999, 239.04)]

# ─── Коэффициенты для электромобилей ЛЕГКОВЫХ (прогрессивная шкала) ───
UTIL_COEF_EV_CAR_NEW = [
    (80, 0.17), (100, 49.56), (130, 65.88), (160, 78.00),
    (190, 92.40), (220, 109.68), (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_EV_CAR_OLD = [
    (80, 0.26), (100, 68.46), (130, 79.76), (160, 92.86),
    (190, 108.16), (220, 126.00), (250, 146.80), (280, 173.40), (9999, 189.84),
]

# ─── Коэффициенты для электромобилей НЕ-ЛЕГКОВЫХ (автобус/грузовой/спецтехника) ───
# Фиксированный коэффициент 15,73 (без прогрессивной шкалы)
UTIL_COEF_EV_OTHER_NEW = [(80, 0.17), (9999, 15.73)]
UTIL_COEF_EV_OTHER_OLD = [(80, 0.26), (9999, 15.73)]

# ─── Коэффициенты для гибридов (порог 160 л.с.) ───
UTIL_COEF_HEV_NEW = [(160, 0.17), (190, 92.40), (220, 109.68), (250, 129.96), (280, 153.96), (9999, 182.40)]
UTIL_COEF_HEV_OLD = [(160, 0.26), (190, 129.72), (220, 151.20), (250, 176.16), (280, 205.20), (9999, 239.04)]

# ─── Коэффициенты для ЮРЛИЦ ───
UTIL_COEF_LEGAL = {
    "Легковой": {"До 3 лет": 2.41, "Старше 3 лет": 3.5},
    "Грузовой": {"До 3 лет": 3.0, "Старше 3 лет": 4.0},
    "Автобус": {"До 3 лет": 3.0, "Старше 3 лет": 4.0},
    "Спецтехника": {"До 3 лет": 4.0, "Старше 3 лет": 5.0},
}

KW_TO_HP = 1.35962


def calculate_util(data: dict) -> dict | None:
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
        if category == "Легковой":
            table = UTIL_COEF_EV_CAR_NEW if age == "До 3 лет" else UTIL_COEF_EV_CAR_OLD
        else:
            # Автобус, грузовой, спецтехника — фиксированный коэффициент
            table = UTIL_COEF_EV_OTHER_NEW if age == "До 3 лет" else UTIL_COEF_EV_OTHER_OLD
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
